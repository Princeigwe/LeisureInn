from django.shortcuts import render, get_object_or_404, redirect
from .models import Service, Subscription, GuestCreatedSubscription
from django.contrib.auth.decorators import login_required
from django.conf import settings
from datetime import datetime
import requests
from requests.adapters import HTTPAdapter
from requests.exceptions import ConnectionError
from .tasks import service_subscription_confirmation_email

flutterwave_adapter = HTTPAdapter(max_retries=5)
session = requests.Session()

session.mount("https://api.ravepay.co/v2/gpx/paymentplans/create", flutterwave_adapter)

# Create your views here.

def all_services_page(request):
    """all services page"""
    services = Service.objects.all()
    return render(request, 'hotel_services/hotel_services.html', {'services': services})


#  get another template for service detail
def service_subscriptions(request, service_id, service_name):
    """getting subscription plans for service"""
    service = get_object_or_404(Service, name=service_name, id=service_id)
    subscriptions = Subscription.objects.filter(service=service)
    return render(request, 'hotel_services/hotel_services_detail.html', {'subscriptions': subscriptions})


def subscription_payment_process(request, subscription_id):
    """this is the subscription creation process.
        This view makes a POST request to flutterwave recurring payment endpoint 
        with the necessary data with Python's requests library, and the guest completes
        the payment with javascript payment modal
    """
    subscription = get_object_or_404(Subscription, id=subscription_id)
    amount = int(subscription.price)
    name = str(subscription.service)
    interval = "every {subscription_days} days".format(subscription_days=subscription.days)
    seckey =  settings.FLUTTERWAVE_TEST_SECRET_KEY
    
    url = "https://api.ravepay.co/v2/gpx/paymentplans/create" ## payment plan endpoint
    payload = dict(amount=amount, name=name, interval=interval, seckey=seckey)
    try:
        subscription_post_request= session.post(url=url, json=payload)
        print(subscription_post_request.text)
    except ConnectionError as ce:
        print(ce)
    
    subscription_post_request_response_json = subscription_post_request.json() # return response object of subscription_post_request in json format 
    print(subscription_post_request_response_json['data']['id']) # printing the payment id
    
    # storing payment_id of subscription in session
    request.session['payment_id'] = subscription_post_request_response_json['data']['id']
    
    user = request.user
    
    # getting the current time
    now = datetime.now() # will be used for transaction reference
    
    publicAPIKey = settings.FLUTTERWAVE_TEST_PUBLIC_KEY # flutterwave public API key
    customer_email = user.email
    amount = amount
    customer_phone = user.mobile
    tx_ref = "lSriN9302-{subscription_id}-{now}".format(subscription_id=subscription.id, now=now)
    metaname = "{service} subscription".format(service=subscription.service)
    metavalue = "subscription ID{id}".format(id=subscription.id)
    payment_plan_id = subscription.id # for payment plan parameter
    
    return render(request, 'hotel_services/service_payment_process.html', {
        'publicAPIKey': publicAPIKey,
        'customer_email': customer_email,
        'amount': amount,
        'customer_phone': customer_phone,
        'tx_ref': tx_ref,
        'metaname': metaname,
        'metavalue': metavalue,
        'payment_plan_id': payment_plan_id,
        'id': subscription.id
    })


def subscription_payment_successful(request, id):
    subscription = get_object_or_404(Subscription, id=id)
    guest = request.user
    payment_id = request.session['payment_id']
    guestCreatedSubscription = GuestCreatedSubscription.objects.create(subscription=subscription, guest=guest, payment_id=payment_id)
    guestCreatedSubscription.save()
    service_subscription_confirmation_email.delay(guestCreatedSubscription.id) # add task to queue
    return render(request, 'hotel_services/service_payment_successful.html', {
        'subscription': subscription,
    })


@login_required
def fetch_guest_subscriptions(request):
    """fetching all the created subscriptions of the guest"""
    user = request.user
    guestCreatedSubscriptions = GuestCreatedSubscription.objects.filter(guest__email=user.email)
    return render(request, 'hotel_services/guest_created_subscriptions.html', {'guestCreatedSubscriptions': guestCreatedSubscriptions})


def cancel_subscription_payment_plan(request, id):
    """this is the flutterwave cancel subscription recurring payment process"""
    flutterwave_cancel_payment_adapter = HTTPAdapter(max_retries=5)
    session = requests.Session()
    seckey = settings.FLUTTERWAVE_TEST_SECRET_KEY

    session.mount("https://api.ravepay.co/v2/gpx/paymentplans/{id}/cancel", flutterwave_cancel_payment_adapter)
    
    guestCreatedSubscription = get_object_or_404(GuestCreatedSubscription, id=id)
    payment_id = guestCreatedSubscription.payment_id # to be used as id in the url endpoint
    
    url = "https://api.ravepay.co/v2/gpx/paymentplans/{id}/cancel".format(id=payment_id)
    
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }
    
    payload = dict(seckey=seckey)
    try:
        subscription_cancel_request= session.post(url=url, json=payload, headers=headers)
        print(subscription_cancel_request.text)
    except ConnectionError as ce:
        print(ce)
    
    #  making update to guestCreatedSubscription model
    guestCreatedSubscription.date_cancelled = datetime.now()
    guestCreatedSubscription.cancelled = True
    guestCreatedSubscription.save()
    return render(request, 'hotel_services/service_payment_cancelled.html')