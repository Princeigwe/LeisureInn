from django.contrib import admin
from .models import Room, Amenities

# Register your models here.

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('room_number', 'room_type', 'room_price', 'is_available', 'amenities_type')
    list_filter = ('is_available', 'room_type')

@admin.register(Amenities)
class AmenitiesAdmin(admin.ModelAdmin):
    list_display = ('item_type', 'first_item', 'second_item', 'third_item', 'fourth_item', 'fifth_item',)
