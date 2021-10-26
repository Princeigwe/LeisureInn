from .models import CustomUser, Profile
from guest_reservations.models import GuestReservationList
from django.dispatch import receiver
from django.db.models.signals import post_save

# reservation list creation code
@receiver(post_save, sender=CustomUser)
def create_reservation_list(sender, instance, created, **kwargs):
    if created:
        GuestReservationList.objects.create(guest=instance)

@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.get_or_create(user=instance)