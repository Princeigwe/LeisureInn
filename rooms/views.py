from django.shortcuts import render, redirect
from .models import Room
from bookings.forms import CheckingForm
from django.views.decorators.cache import cache_page

CACHE_TIME = 60 * 15 # setting cache time to 15 minutes

@cache_page(CACHE_TIME)
def home_featured_rooms(request):
    featured_rooms = Room.objects.filter(room_price__range=[11000, 18000], is_available=True)
    if request.method == 'POST':
        form = CheckingForm(request.POST)
        if form.is_valid():
            room_type = form.cleaned_data.get('room_type')
            check_in = form.cleaned_data.get('check_in')
            check_out = form.cleaned_data.get('check_out')
            
            request.session["room_type_data"] = room_type
            request.session["check_in_data"] = str(check_in)
            request.session["check_out_data"] = str(check_out)
            
            return redirect('rooms:check_room_availability')
    else:
        form = CheckingForm()
    return render(request, 'home.html', {'featured_rooms':featured_rooms, 'form':form})


@cache_page(CACHE_TIME)
def available_rooms(request):
    available_rooms = Room.objects.filter(is_available=True)
    return render(request, 'rooms/rooms.html', {'available_rooms':available_rooms})


@cache_page(CACHE_TIME)
def check_room_availability(request):
    """checking room type based on room type session key"""
    room_type = request.session["room_type_data"]
    available_rooms = Room.objects.filter(is_available=True, room_type=room_type)
    return render(request, 'rooms/rooms.html', {'available_rooms':available_rooms})
