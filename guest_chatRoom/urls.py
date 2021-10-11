from django.urls import path
from .views import rooms

app_name = 'guest_chatRoom'

urlpatterns = [
    path('rooms/', rooms, name='rooms')
]