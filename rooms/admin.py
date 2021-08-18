from django.contrib import admin
from .models import Room

# Register your models here.

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('room_number', 'room_type', 'room_price', 'is_available')
    list_filter = ('is_available', 'room_type')