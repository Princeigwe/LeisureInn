from django.shortcuts import render, get_object_or_404, redirect

from LeisureInn.settings import SECRET_KEY
from .models import Service, Subscription, GuestPaidSubscription
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings

from datetime import datetime
import requests
from requests.adapters import HTTPAdapter
from requests.exceptions import ConnectionError

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

def subscription_payment_successful(request):
    # subscription = get_object_or_404(Subscription, id=id)
    # guest = request.user
    # guestPaidSubscription = GuestPaidSubscription.objects.create(subscription=subscription, guest=guest, paid=True, date_created=datetime.now)
    # guestPaidSubscription.save()
    return render(request, 'hotel_services/service_payment_successful.html')