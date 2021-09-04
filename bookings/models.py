from django.db import models
from rooms.models import Room

# Create your models here.

class Booking(models.Model):
    room = models.ForeignKey(Room, related_name='room', on_delete=models.CASCADE)
    guest_firstname = models.CharField(max_length=50)
    guest_lastname = models.CharField(max_length=50)
    guest_email = models.EmailField(max_length=50, default=None)
    guest_telephone = models.CharField(max_length=12, default=None)
    checked_in = models.BooleanField(default=False)
    check_in = models.DateField()
    check_out = models.DateField()
    amount = models.DecimalField(max_digits=9, decimal_places=2)
    paid = models.BooleanField(default=False)
    
    def __str__(self):
        return str(self.room)
