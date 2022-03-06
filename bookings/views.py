from django.shortcuts import render, get_object_or_404, redirect
from .models import Booking
from .forms import BookingForm
from rooms.models import Room
import datetime
from .tasks import booking_confirmation_email
from django.contrib.auth.decorators import login_required
from guest_reservations.models import ReservationItem, GuestReservationList

# Create your views here.

# remove the @login_required decorators to test the views

@login_required
def booking_process(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.room = room
            booking.guest_firstname = request.user.first_name
            booking.guest_lastname = request.user.last_name
            booking.guest_email = request.user.email
            booking.guest_telephone = form.cleaned_data.get('guest_telephone')
            booking.amount = form.cleaned_data.get('amount')
            booking.check_in = request.session["check_in_data"]
            booking.check_out = request.session["check_out_data"]
            
            request.session['room_id_data'] = room.id
            
            # conversion string format of check dates to date type data
            date_book_check_in = datetime.datetime.strptime(booking.check_in, "%Y-%m-%d").date()
            date_book_check_out = datetime.datetime.strptime(booking.check_out, "%Y-%m-%d").date()
            
            number_of_days = (date_book_check_out - date_book_check_in).days ## getting the number of days from calendar
            amount_written = form.cleaned_data.get('amount')
            amount_to_pay = int(room.room_price) * number_of_days
            
            if amount_written == amount_to_pay :
                booking.save()
                
                # creating booking id session data that will be used for adding reservation to reservation list
                # the reservation addition function will take place in  payment_successful view function
                request.session["booking_id_data"] = booking.id
                

                booking_confirmation_email.delay(room.id, booking.id) # launching aynctask to celery
                
                #return redirect('bookings:booking_successful')
                return redirect('payments:process', booking.id) # redirecting to the payment url with booking id
            
            else:
                return redirect('bookings:booking_failed')
        
    else:
        form = BookingForm()
    return render(request, 'booking/booking_form.html', {'form': form})

@login_required
def booking_failed(request):
    return render(request, 'booking/booking_failed.html')

@login_required
def booking_successful(request):
    return render(request, 'booking/booking_successful.html')
