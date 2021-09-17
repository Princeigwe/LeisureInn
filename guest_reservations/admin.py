from django.contrib import admin
from .models import ReservationItem, GuestReservationList

# Register your models here.


class ReservationItemAdminInline(admin.TabularInline):
    model = ReservationItem
    list_display = ('booking')

class GuestReservationListAdmin(admin.ModelAdmin):
    model = GuestReservationList
    list_display = ['guest', ]
    search_fields = ('guest', )
    inlines = [ReservationItemAdminInline]

admin.site.register(GuestReservationList, GuestReservationListAdmin)