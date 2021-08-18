from django.db import models

# Create your models here.

from django.db import models
from  django.db import models

# # Create your models here.

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
    
    def __str__(self):
        return self.room_type
