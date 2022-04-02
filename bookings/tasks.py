from celery import Celery
from rooms.models import Room
from django.core.mail import send_mail
from .models import Booking

# app = Celery(app="LeisureInn", broker="amqp://guest:guest@rabbitmq:5672/")
app = Celery(app="LeisureInn", broker="amqps://drzmfmjq:zKOJkSm-OZo7Obpd1q_ulUz4APdmXop7@fox.rmq.cloudamqp.com/drzmfmjq")

@app.task # this is a celery task
def booking_confirmation_email(room_id, booking_id):
    booking = Booking.objects.get(id=booking_id)
    room = Room.objects.get(id=room_id)
    subject = "Booking Confirmed"
    message = f'You have successfully booked room {room.id}'
    send_mail(subject, message, "admin@leisureinn@gmail.com", [booking.guest_email], fail_silently=False)

