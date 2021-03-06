from logging import root
from django.shortcuts import render, get_object_or_404
from django.conf import settings
from bookings.models import Booking
from rooms.models import Room
from guest_reservations.models import GuestReservationList, ReservationItem


#  payment process with flutterwave payment parameters
def payment_process(request, booking_id):
    publicKey = settings.FLUTTERWAVE_TEST_PUBLIC_KEY
    booking = get_object_or_404(Booking, id=booking_id)
    customer_email = booking.guest_email
    customer_phone = booking.guest_telephone
    amount = booking.amount
    tx_ref = "lSriN9302" + str(booking.id)
    return render(request, 'payment/payment_process.html',
                {
                    'publicKey': publicKey,
                    'customer_email': customer_email,
                    'customer_phone': customer_phone,
                    'amount': amount,
                    'tx_ref': tx_ref,
                    'id':booking.id,
                }
    )

def payment_successful(request, id):
    booking = get_object_or_404(Booking, id=id)
    booking.paid = True
    booking.save()
    
    #process of adding booking reservation list here###
    booking_id = request.session['booking_id_data']
    reservation_list = get_object_or_404(GuestReservationList, guest=request.user)
    booking = get_object_or_404(Booking, id=booking_id)
    reservation_item = ReservationItem.objects.create(reservation_list=reservation_list, booking=booking)
    reservation_item.save()
    ######
    
    room_id = request.session['room_id_data']
    room = get_object_or_404(Room, id=room_id)
    room.is_available = False
    room.is_booked = True
    room.save() # saving new status of the room
    
    # deleting session data
    # del request.session["check_in_data"] .................to be used in hotel services app
    # del request.session["check_out_data"] ................ to be used in hotel services app
    del request.session["room_type_data"]
    del request.session['room_id_data']
    # del request.session['booking_id_data']
    
    return render(request, 'payment/payment_successful.html', {'id':id})

def payment_failed(request):
    return render(request, 'payment/payment_failed.html')