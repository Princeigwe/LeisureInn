from django.urls import path

from .views import home_featured_rooms, available_rooms

app_name='rooms'

urlpatterns = [
    path('', home_featured_rooms, name='home'),
    path('available_rooms/', available_rooms, name='available_rooms')
]