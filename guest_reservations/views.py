from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import ReservationItem, GuestReservationList
from bookings.models import Booking

# Create your views here.


@login_required
def all_reservations(request):
    """ function to get all reservations of the logged in guest """
    guest_reservations = ReservationItem.objects.all()
    return render(request, 'guest_reservation/reservations.html', {'guest_reservations': guest_reservations})


# add_to_reservations function executed in the payment_successful view function of payment app

# @login_required
# def add_to_reservations(request, booking_id):
#     reservation_list = get_object_or_404(GuestReservationList, guest=request.user)
#     booking = get_object_or_404(Booking, id=booking_id)
#     reservation_item = ReservationItem.objects.create(reservation_list=reservation_list, booking=booking)
#     return redirect('guest_reservations:all_reservations')


@login_required
def delete_reservation(request, reservation_item_id):
    reservation_item = get_object_or_404(ReservationItem, id=reservation_item_id)
    reservation_item.delete()
    return redirect('guest_reservations:all_reservations')


@login_required
def clear_reservations(request):
    reservation_items = ReservationItem.objects.all()
    reservation_items.delete()
    return redirect('guest_reservations:all_reservations')


# thinkung of switching reservations, but can't come up with an idea yet.