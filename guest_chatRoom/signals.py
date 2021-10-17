
from django.db.models.signals import post_save
from django.dispatch import receiver
from users.models import CustomUser
from .models import GuestChatRoom
from allauth.account.signals import user_signed_up


# creating guestchatrooms with django allauth signals
adminusers = CustomUser.objects.filter(is_superuser = True)

@receiver(user_signed_up)
def user_signed_up(request, user, **kwargs):
    for adminuser in adminusers:
        chatroom = GuestChatRoom.objects.create(guest=user, admin=adminuser)
        chatroom.save()
