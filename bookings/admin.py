from django.contrib import admin
from  .models import Booking
from rooms.models import Room

# Register your models here.


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['room_number', 'guest_firstname', 'guest_lastname', 'guest_email', 'guest_telephone', 'checked_in', 'check_in', 'check_out', 'checked_out', 'amount', 'paid']
    search_fields = ['guest_firstname', 'guest_lastname']
    list_filter = ['paid', 'checked_in', 'checked_out']
    
    # for displaying the room number in the list_display
    def room_number(self, obj):
        return obj.room.room_number
