from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
from .managers import CustomUserManager
from rooms.models import Room
# Create your models here.

class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique=True)
    first_name = models.CharField(max_length=50, default='first name')
    last_name = models.CharField(max_length=50, default='last name')
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    objects = CustomUserManager()
    
    def __str__(self):
        return self.email


class GuestReservationList(models.Model):
    guest = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    
    def __str__(self):
        return str(self.guest.first_name + self.guest.last_name)


class ReservationItem(models.Model):
    reservation_list = models.ForeignKey(GuestReservationList, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    
    def __str__(self):
        return str(self.room.number)
