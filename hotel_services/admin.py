from django.contrib import admin
from .models import Service, Subscription, GuestCreatedSubscription

# Register your models here.

class SubscriptionInline(admin.TabularInline):
    model = Subscription
    list_display = ['plan', 'price', 'description']

class ServiceAdmin(admin.ModelAdmin):
    list_display = ['id', 'image', 'name', 'description',]
    model = Service
    inlines = [SubscriptionInline]

class GuestCreatedSubscriptionAdmin(admin.ModelAdmin):
    model = GuestCreatedSubscription
    list_display = ['id', 'subscription']
    
    def subscription(self, obj):
        return obj.service.name



admin.site.register(Service, ServiceAdmin)
admin.site.register(GuestCreatedSubscription, GuestCreatedSubscriptionAdmin)