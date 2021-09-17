from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import ReservationItem, GuestReservationList
from bookings.models import Booking

# Create your views here.


@login_required
def all_reservations(request):
    """ function to get all reservations of the logged in guest """
    guest_reservations = ReservationItem.objects.all()
    context = {'guest_reservations': guest_reservations}
    return render(request, 'reservations.html', context=context)


@login_required
def add_to_reservations(request, booking_id):
    reservation_list = get_object_or_404(GuestReservationList, guest=request.user)
    booking = get_object_or_404(Booking, id=booking_id)
    reservation_item = ReservationItem.objects.create(reservation_list=reservation_list, booking=booking)
    pass


@login_required
def delete_reservation(request):
    pass


@login_required
def clear_reservations(request):
    pass


# thinkung of switching reservations, but can't come up with an idea yet.