from django.contrib import admin
from .models import ReservationItem, GuestReservationList

# Register your models here.


class ReservationItemAdminInline(admin.TabularInline):
    model = ReservationItem
    fields = ['booking', ]

class GuestReservationListAdmin(admin.ModelAdmin):
    inlines = [ReservationItemAdminInline]
    model = GuestReservationList
    list_display = ['guest', ]
    search_fields = ('guest', )

admin.site.register(GuestReservationList, GuestReservationListAdmin)