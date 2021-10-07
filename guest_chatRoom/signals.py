
from django.db.models.signals import post_save
from django.dispatch import receiver
from users.models import CustomUser
from .models import GuestChatRoom

@receiver(post_save, sender=CustomUser)
def create_guest_chatRoom(sender, instance, created, **kwargs):
    GuestChatRoom.objects.create(user=instance)


