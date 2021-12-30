from django.urls import path
from .views import rooms, room_messages, guest_chatRoom_user_bio_and_trans_data

app_name = 'guest_chatRoom'

urlpatterns = [
    path('rooms/', rooms, name='rooms'),
    # path('rooms/<int:room_id>/', rooms, name='rooms_with_id'),
    path('room_messages/<int:room_id>/', room_messages, name='room_messages'),
    path('user-bio-trans-data/<int:room_id>/', guest_chatRoom_user_bio_and_trans_data, name='user_bio_trans_data')
]