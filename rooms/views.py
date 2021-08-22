from django.shortcuts import render, redirect
from .models import Room
from bookings.forms import CheckingForm

# Create your views here.

def home_featured_rooms(request):
    featured_rooms = Room.objects.filter(room_price__range=[11000, 18000], is_available=True)
    if request.method == 'POST':
        form = CheckingForm(request.POST)
        if form.is_valid():
            room_type = form.cleaned_data.get('room_type')
            check_in = form.cleaned_data.get('check_in')
            check_out = form.cleaned_data.get('check_out')
            
            # converting dates to string format
            check_in_string = check_in.strftime
            check_out_string = check_out.strftime
            
            return redirect('rooms:check_room_availability', room_type, check_in_string, check_out_string)
    else:
        form = CheckingForm()
    return render(request, 'home.html', {'featured_rooms':featured_rooms, 'form':form})

def available_rooms(request):
    available_rooms = Room.objects.filter(is_available=True)
    return render(request, 'rooms/rooms.html', {'available_rooms':available_rooms})


def check_room_availability(request, room_type, check_in_string, check_out_string):
    return redirect('rooms:available_rooms')