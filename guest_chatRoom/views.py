from django.shortcuts import render, get_object_or_404
from .models import GuestChatRoom, Message
from users.models import CustomUser
from .forms import MessageForm
from django.contrib.auth.decorators import login_required
from django.utils.safestring import mark_safe
import json

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

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
    
    
    # if request.method == 'GET':
    #     sender = request.user
    #     roomMessages = Message.objects.filter(id=room.id)
    #     return render(request, 'guest_chatroom/chat_detail.html', {'room_id': room.id, 'room':room, 'sender': sender, 'roomMessages': roomMessages})
    
    # else:
    #     sender = request.user
    #     form = MessageForm(request.POST)
    #     if form.is_valid():
    #         form.save(commit=False)
    #         content = form.cleaned_data['content']
    #         message = Message.objects.create(sender=sender, content=content)
    #         message.save()
    #         roomMessages = Message.objects.filter(id=room.id)
    #         group_name = 'chatRoom_%s' % room.id
    #         channel_layer = get_channel_layer()
    #         payload = {
    #             'type': 'chat_message',
    #             'message': content,
    #             'sender': sender
    #         }
    #         async_to_sync(channel_layer.group_send)(group_name, payload)
    #     return render(request, 'guest_chatroom/chat_detail.html', {'room_id': room.id, 'room':room, 'roomMessages': roomMessages, 'group_name': group_name})








    # user = request.user
    # if request.method=='GET':
    #     left_message = Message.objects.get(receiver=user)
    #     right_message = Message.objects.get(sender=user) 
        
    #     all_messages = Message.objects.filter(id=room_id)
    #     return render(request, 'guest_chatroom/chat_detail.html', {'room_id': room.id, 'room':room, 'all_messages': all_messages, 'left_message': left_message, 'right_message': right_message})
    
    # else:
    #     form = MessageForm(request.POST)
    #     if user.is_superuser:
    #         sender = user
    #         receiver = room.guest
    #         if form.is_valid():
    #             form.save(commit=False)
    #             content = form.cleaned_data.get['content']
    #             message = Message.objects.create(sender=sender, receiver=receiver, content=content)
    #             # message.save()
                
    #             channel_layer = get_channel_layer()
    #             payload = {
    #                 'type':'receive',
    #                 'message': content,
    #                 'sender': user
    #             }
    #             room_group
                
    #     else:
    #         sender = user
    #         receiver = room.admin
    #         if form.is_valid():
    #             form.save(commit=False)
    #             content = form.cleaned_data.get['content']
    #             message = Message.objects.create(sender=sender, receiver=room.admin, content=content)
    #             message.save()
                
    #     all_messages = Message.objects.filter(id=room_id)
    # return render(request, 'guest_chatroom/chat_detail.html', {'room_id': room.id, 'room':room})