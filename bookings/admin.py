from django.contrib import admin
from  .models import Booking

# Register your models here.

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['room', 'guest_firstname', 'guest_lastname', 'check_in', 'check_out', 'amount']
    search_fields = ['guest_firstname', 'guest_lastname']