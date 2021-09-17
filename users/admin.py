from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser, Reservation
# Register your models here.

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('email', 'first_name', 'last_name', 'is_staff', 'is_active')
    list_filter = ('email', 'is_staff', 'is_active',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active')
        }),
    )
    search_fields = ('email', )
    ordering = ('email', )

admin.site.register(CustomUser, CustomUserAdmin)


class ReservationAdmin(admin.ModelAdmin):
    model = Reservation
    list_display = ['guest', 'room']
    search_fields = ('guest', )

admin.site.register(Reservation, ReservationAdmin)