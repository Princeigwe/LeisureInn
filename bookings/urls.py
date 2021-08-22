from django.urls import path
from .views import booking_process, booking_failed, booking_successful

app_name='bookings'

urlpatterns = [
    path('booking_process/<int:room_id>/', booking_process, name="booking_process"),
    path('booking_successful/', booking_successful, name="booking_successful"),
    path('booking_failed/', booking_failed, name="booking_failed")
]