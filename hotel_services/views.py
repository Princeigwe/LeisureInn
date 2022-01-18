from unicodedata import name
from django.shortcuts import render, get_object_or_404
from .models import Service, Subscription
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings

from datetime import date, datetime

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
def subscription_service_payment_process(request, subscription_id):
    """booking a service based on subscription plan"""
    # getting guests number of days of stay
    guest_checkIn_date = date(request.session["check_in_data"])
    guest_checkOut_date = date(request.session["check_out_data"])
    guestDaysOfStay = (guest_checkOut_date - guest_checkIn_date).days
    
    # getting the subscription the guest wants to pay for
    subscription = get_object_or_404(Subscription, id=subscription_id)
    subscription_days = subscription.days
    subscription_price = subscription.price
    
    # getting service name
    service = subscription.service
    
    
    # getting details for flutterwave payment parameters
    now = datetime.now()
    publicKey = settings.FLUTTERWAVE_TEST_PUBLIC_KEY
    customer_email = request.user.email
    customer_phone = request.user.phone
    amount = subscription_price
    tx_ref = "lSriN9302" + str(service.name+subscription.id+now)
    
    # posting message warning
    if subscription_days < guestDaysOfStay:
        messages.warning(request, "Your number of stay is less than days of subscription plan. No refunds once booked")
    
    return render(request, 'hotel_services/service_payment_process.html', {
        'publicKey': publicKey,
        'customer_email': customer_email,
        'customer_phone': customer_phone,
        'amount': amount,
        'tx_ref': tx_ref
    })