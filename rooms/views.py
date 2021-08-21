from django.shortcuts import render
from .models import Room
from bookings.forms import CheckingForm

# Create your views here.

def home_featured_rooms(request):
    featured_rooms = Room.objects.filter(room_price__range=[11000, 18000], is_available=True)
    checking_form = CheckingForm()
    return render(request, 'home.html', {'featured_rooms':featured_rooms, 'checking_form': checking_form})

def available_rooms(request):
    available_rooms = Room.objects.filter(is_available=True)
    return render(request, 'rooms/rooms.html', {'available_rooms':available_rooms})


def check_room_availability(request):
    return render(request,'rooms/rooms.html')