from django.shortcuts import render, get_object_or_404
from .models import GuestChatRoom
from users.models import CustomUser

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


def rooms(request):
    # chat_room = get_object_or_404(GuestChatRoom, id=room_id)
    user = request.user
    adminuser = CustomUser.is_superuser = True
    
    # getting all chatrooms...
    if user.is_superuser:
        rooms = GuestChatRoom.objects.all().exclude(user=request.user) # if logged in user is an admin, get all rooms apart from his own
    else:
        rooms = GuestChatRoom.objects.filter(user = adminuser)
    
    # # choosing a room
    # picked_room = get_object_or_404(GuestChatRoom, id=room_id)
    
    
    return render(request,'guest_chatroom/index.html', {'rooms': rooms})