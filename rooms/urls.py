from django.urls import path

from .views import check_room_availability, home_featured_rooms, available_rooms

app_name='rooms'

urlpatterns = [
    path('', home_featured_rooms, name='home'),
    path('available_rooms/', available_rooms, name='available_rooms'),
    # path('availability_check/<str:room_type>/<str:check_in_string>/<str:check_out_string>/', check_room_availability, name='check_room_availability')
    path('availability_check/', check_room_availability, name='check_room_availability'),
]