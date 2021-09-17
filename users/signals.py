from .models import Reservation, CustomUser
from django.dispatch import receiver
from django.db.models.signals import post_save

# reservation list creation code
@receiver(post_save, sender=CustomUser)
def create_reservation_list(sender, instance, created, **kwargs):
    if created:
        Reservation.objects.create(guest=instance)
