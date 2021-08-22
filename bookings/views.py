from django.shortcuts import render, get_object_or_404, redirect
from .models import Booking
from .forms import BookingForm
from rooms.models import Room
import datetime

# Create your views here.

def booking_process(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            # form.save(commit=False)
            booking = form.save(commit=False)
            booking.room = room
            booking.guest_firstname = form.cleaned_data.get('guest_firstname')
            booking.guest_lastname = form.cleaned_data.get('guest_lastname')
            booking.amount = form.cleaned_data.get('amount')
            booking.check_in = request.session["check_in_data"]
            booking.check_out = request.session["check_out_data"]
            
            # conversion string format of check dates to date type data
            date_book_check_in = datetime.datetime.strptime(booking.check_in, "%Y-%m-%d").date()
            date_book_check_out = datetime.datetime.strptime(booking.check_out, "%Y-%m-%d").date()
            
            number_of_days = (date_book_check_out - date_book_check_in).days ## getting the number of days from calendar
            amount_written = form.cleaned_data.get('amount')
            amount_to_pay = int(room.room_price) * number_of_days
            
            if amount_written == amount_to_pay :
                booking.save()
                # deleting session data
                del request.session["check_in_data"]
                del request.session["check_out_data"]
                del request.session["room_type_data"]
                
                return redirect('bookings:booking_successful')
            
            else:
                return redirect('bookings:booking_failed')
        
    else:
        form = BookingForm()
    return render(request, 'booking/booking_form.html', {'form': form})


def booking_failed(request):
    return render(request, 'booking/booking_failed.html')

def booking_successful(request):
    return render(request, 'booking/booking_successful.html')
