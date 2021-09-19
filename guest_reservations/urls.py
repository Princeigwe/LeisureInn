from django.urls import path
from .views import all_reservations, delete_reservation

app_name = 'guest_reservations'

urlpatterns = [
    path('all_reservations/', all_reservations, name='all_reservations'),
    # path('add_to_reservations/', add_to_reservations, name='add_to_reservations'),
    path('<int:reservation_id>/delete_reservation/', delete_reservation, name='delete_reservation'),
]