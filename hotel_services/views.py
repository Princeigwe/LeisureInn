from django.shortcuts import render, get_object_or_404, redirect
from .models import OneTimeService, Service, Subscription, GuestCreatedSubscription, GuestOneTimeServicePayment
from django.contrib.auth.decorators import login_required
from django.conf import settings
from datetime import datetime
import requests
from requests.adapters import HTTPAdapter
from requests.exceptions import ConnectionError
from .tasks import service_subscription_confirmation_email, one_time_payment_confirmation_email, subscription_payment_API_call, cancel_subscription_payment_API_call

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


@login_required
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

    # creating session keys to be used in tasks.py subscription_payment_process api call
    request.session['amount'] = amount
    request.session['name'] = name
    request.session['interval'] = interval
    request.session['seckey'] = seckey
    
    subscription_payment_API_call.delay(amount, name, interval, seckey) # calling the background task, subscription_payment_API_call
    subscription_response = subscription_payment_API_call.delay(amount, name, interval, seckey)
    
    subscription_post_request_response_json = subscription_response.get()## getting the result of the background task
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


@login_required
def subscription_payment_successful(request, id):
    subscription = get_object_or_404(Subscription, id=id)
    guest = request.user
    payment_id = request.session['payment_id']
    guestCreatedSubscription = GuestCreatedSubscription.objects.create(subscription=subscription, guest=guest, payment_id=payment_id)
    guestCreatedSubscription.save()
    # service_subscription_confirmation_email.delay(guestCreatedSubscription.id) # add task to queue
    return render(request, 'hotel_services/service_payment_successful.html', {
        'subscription': subscription,
    })


@login_required
def fetch_guest_subscriptions(request):
    """fetching all the created subscriptions of the guest"""
    user = request.user
    guestCreatedSubscriptions = GuestCreatedSubscription.objects.filter(guest__email=user.email)
    return render(request, 'hotel_services/guest_created_subscriptions.html', {'guestCreatedSubscriptions': guestCreatedSubscriptions})


@login_required
def cancel_subscription_payment_plan(request, id):
    """this is the flutterwave cancel subscription recurring payment process"""
    
    seckey = settings.FLUTTERWAVE_TEST_SECRET_KEY    
    guestCreatedSubscription = get_object_or_404(GuestCreatedSubscription, id=id)
    payment_id = guestCreatedSubscription.payment_id # to be used as id in the url endpoint
    
    cancel_subscription_payment_API_call.delay(payment_id, seckey) # calling the background task, cancel_subscription_payment_API_call

    #  making update to guestCreatedSubscription model
    guestCreatedSubscription.date_cancelled = datetime.now()
    guestCreatedSubscription.cancelled = True
    guestCreatedSubscription.save()
    return render(request, 'hotel_services/service_payment_cancelled.html')


def one_time_services(request):
    """this is a view to create services for one time payment,
    the current service page shows link for the subscription plans
    """
    services = Service.objects.all()
    return render(request, 'hotel_services/one_time_services.html', {'services': services})


def one_time_service_payment_process(request, service_id):
    """this is the process for one time service payment"""
    now = datetime.now()
    user = request.user
    publicKey = settings.FLUTTERWAVE_TEST_PUBLIC_KEY
    service = get_object_or_404(Service, id=service_id)
    customer_email = user.email
    customer_phone = user.mobile
    amount = int(service.one_time_service.price)
    request.session['amount_session_data'] = amount
    tx_ref = "lSriN9302-{service_id}-{now}".format(service_id=service.id, now=now)
    return render(request, 'hotel_services/one_time_service_payment_process.html',
                {
                    'publicKey': publicKey,
                    'customer_email': customer_email,
                    'customer_phone': customer_phone,
                    'amount': amount,
                    'tx_ref': tx_ref,
                    'id':service.id,
                }
    )


def one_time_service_payment_successful(request, id):
    """this function creates a GuestOneTimeServicePayment to keep track of the
        the one time payments guest made  after transaction is successful from the
        'one_time_service_payment_process' view function
    """
    one_time_service = OneTimeService.objects.get(service_id=id)
    guest = request.user
    paid = True
    paid_date = datetime.now()
    guestOneTimeServicePayment = GuestOneTimeServicePayment.objects.create(service=one_time_service, guest=guest, paid=paid, paid_date=paid_date)
    guestOneTimeServicePayment.save()
    one_time_payment_confirmation_email.delay(guestOneTimeServicePayment.id) # add task to queue
    return render(request, 'hotel_services/one_time_service_payment_successful.html')


def one_time_service_payment_failed(request):
    return render(request, 'hotel_services/one_time_service_payment_failed.html')