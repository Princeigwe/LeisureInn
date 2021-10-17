from django.shortcuts import render, get_object_or_404
from .models import GuestChatRoom, Message
from users.models import CustomUser
from .forms import MessageForm
from django.contrib.auth.decorators import login_required

# Create your views here.

def room_testing(request):
    """getting list of rooms for both guest and admin.
    if the logged in user is an admin, get all rooms.
    if the logged in user is a guest, get rooms of the admin users
    """
    user = request.user
    if user.is_superuser:
        rooms = GuestChatRoom.objects.all()
    else:
        rooms = GuestChatRoom.objects.filter(user = user.is_superuser)
    pass


@login_required
def rooms(request):
    user = request.user
    # getting all chatrooms...
    if user.is_superuser:
        rooms = GuestChatRoom.objects.filter(admin = user) # if logged in user is an admin, get all chat rooms related to him
    else:
        rooms = GuestChatRoom.objects.filter(guest = user)
    return render(request,'guest_chatroom/chat_list.html', {'rooms': rooms})


@login_required
def room_messages(request, room_id):
    room = get_object_or_404(GuestChatRoom, id=room_id)
    return render(request, 'guest_chatroom/chat_detail.html', {'room_id': room.id })