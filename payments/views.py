from django.shortcuts import render, get_object_or_404
from django.conf import settings
from bookings.models import Booking

# Create your views here.

def payment_process(request, booking_id):
    publicKey = settings.FLUTTERWAVE_TEST_PUBLIC_KEY
    booking = get_object_or_404(Booking, id=booking_id)
    customer_email = booking.guest_email
    
    amount = booking.amount
    
    pass

def payment_successful(request):
    pass

def payment_failed(request):
    pass