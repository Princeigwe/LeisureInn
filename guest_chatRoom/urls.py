from django.urls import path
from .views import rooms, room_messages

app_name = 'guest_chatRoom'

urlpatterns = [
    path('rooms/', rooms, name='rooms'),
    # path('rooms/<int:room_id>/', rooms, name='rooms_with_id'),
    path('room_messages/<int:room_id>/', room_messages, name='room_messages'),
]