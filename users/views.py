from django.shortcuts import render, get_object_or_404
from .models import Reservation
from django.contrib.auth.decorators import login_required
from bookings.models import Booking


# Create your views here.

@login_required
def all_reservations(request):
    """ function to get all reservations of the logged in guest """
    guest_reservations = Reservation.objects.filter(guest=request.user)
    context = {'guest_reservations': guest_reservations}
    return render(request, 'reservations.html', context=context)


@login_required
def add_to_reservations(request, booking_id):
    reservation_list = get_object_or_404(Reservation, guest=request.user)
    booking = get_object_or_404(Booking, id=booking_id)
    pass


@login_required
def delete_reservation(request):
    pass


@login_required
def clear_reservations(request):
    pass


# thinkung of switching reservations, but can't come up with an idea yet.