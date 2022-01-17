from django.contrib import admin
from .models import Service, Subscription

# Register your models here.

class SubscriptionInline(admin.TabularInline):
    model = Subscription
    list_display = ['plan', 'price', 'description']

class ServiceAdmin(admin.ModelAdmin):
    list_display = ['id', 'image', 'name', 'description',]
    model = Service
    inlines = [SubscriptionInline]



admin.site.register(Service, ServiceAdmin)