from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser, GuestReservationList, ReservationItem
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

class ReservationItemAdminInline(admin.TabularInline):
    model = ReservationItem
    list_display = ('room')

class GuestReservationListAdmin(admin.ModelAdmin):
    model = GuestReservationList
    list_display = ['guest', ]
    search_fields = ('guest', )
    inlines = [ReservationItemAdminInline]

admin.site.register(GuestReservationList, GuestReservationListAdmin)