from django.db import models

# Create your models here.

from django.db import models
from  django.db import models
from django.db.models.deletion import SET_NULL

# # Create your models here.

AMENITIES_ROOM_TYPES = (
    ( "SINGLE ROOM", "Single Room" ),
    ( "DOUBLE ROOM", "Double Room" ),
    ( "TRIPLE ROOM", "Triple Room" ),
    ( "QUAD ROOM", "Quad Room" ),
)


class Amenities(models.Model):
    item_type=models.CharField(max_length=20, choices=AMENITIES_ROOM_TYPES,default='SINGLE ROOM')
    first_item=models.CharField(max_length=20, blank=True)
    second_item=models.CharField(max_length=20, blank=True)
    third_item=models.CharField(max_length=20, blank=True)
    fourth_item=models.CharField(max_length=20, blank=True)
    fifth_item=models.CharField(max_length=20, blank=True)
    
    def __str__(self):
        return self.item_type
    
    class Meta:
        verbose_name_plural = "Amenities"

ROOM_TYPES = (
    ( "SINGLE ROOM", "Single Room" ),
    ( "DOUBLE ROOM", "Double Room" ),
    ( "TRIPLE ROOM", "Triple Room" ),
    ( "QUAD ROOM", "Quad Room" ),
)

class Room(models.Model):
    room_number = models.CharField(max_length=3)
    room_picture = models.ImageField(upload_to='room_pictures/', default='')
    room_type = models.CharField(max_length=20, choices=ROOM_TYPES, default='SINGLE ROOM' )
    is_available = models.BooleanField(default=True)
    room_price = models.DecimalField(max_digits=9, decimal_places=2, default='1000.00')
    amenities_type = models.ForeignKey(Amenities, null=True, on_delete=models.SET_NULL,)
    
    def __str__(self):
        return self.room_type
