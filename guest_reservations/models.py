from django.db import models
from users.models import CustomUser
from bookings.models import Booking

# Create your models here.


class GuestReservationList(models.Model):
    guest = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    
    def __str__(self):
        return str(self.guest.first_name + self.guest.last_name)


class ReservationItem(models.Model):
    reservation_list = models.ForeignKey(GuestReservationList, on_delete=models.CASCADE)
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, default = None)
    
    def __str__(self):
        return str(self.room.number)
