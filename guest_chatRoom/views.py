from django.shortcuts import redirect, render, get_object_or_404
from .models import GuestChatRoom, Message
from users.models import CustomUser
from users.forms import UserSendEmailForm
from .forms import MessageForm
from django.contrib.auth.decorators import login_required
from django.utils.safestring import mark_safe
import json
# from webpush import send_user_notification # importing the single user notification from webpush
from django.views.decorators.http import require_POST 


from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer


from users.tasks import send_user_email

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
def room_messages(request, room_id ):
    user_first_name = request.user.first_name
    room = get_object_or_404(GuestChatRoom, id=room_id )
    # localHostRoomUrl = 'http://0.0.0.0:8000/guest_chatRoom/room_messages/' + str(room.id) 
    roomMessages = Message.objects.filter(id=room.id)
    return render(request, 'guest_chatroom/chat_detail.html', {'room_id': room.id, 'room':room, 'roomMessages': roomMessages, 'user_first_name':user_first_name})

@login_required
def guest_chatRoom_user_bio_and_trans_data(request, room_id): # getting user bio data for now
    room = get_object_or_404(GuestChatRoom, id=room_id)
    if request.method == 'POST':
        userSendEmailForm = UserSendEmailForm(request.POST)
        if userSendEmailForm.is_valid():
            recipient = userSendEmailForm.cleaned_data['recipient']
            subject = userSendEmailForm.cleaned_data['subject']
            message = userSendEmailForm.cleaned_data['message']
            sender = request.user.email
            send_user_email.delay(subject, message, sender, recipient) # the background task for sending email to user for user_bio_data_page.html
            
            return redirect('rooms:home')
    else:
        userSendEmailForm = UserSendEmailForm()
    return render(request, 'users/user_bio_trans_data.html', {'room':room, 'userSendEmailForm': userSendEmailForm })