from xml.parsers.expat import model
from django.contrib import admin
from .models import Service, Subscription, GuestCreatedSubscription, GuestOneTimeServicePayment, OneTimeService

# Register your models here.

class SubscriptionInline(admin.TabularInline):
    model = Subscription
    list_display = ['plan', 'price', 'description']


class OneTimeServicePaymentInline(admin.TabularInline):
    model = OneTimeService
    list_display = ['service', 'price']


class ServiceAdmin(admin.ModelAdmin):
    list_display = ['id', 'image', 'name', 'description',]
    model = Service
    inlines = [SubscriptionInline, OneTimeServicePaymentInline]


class GuestCreatedSubscriptionAdmin(admin.ModelAdmin):
    model = GuestCreatedSubscription
    list_display = ['id', 'subscription', 'guest', 'cancelled', 'date_created', 'payment_id', 'date_cancelled']
    
    def subscription(self, obj):
        return obj.service.name


class GuestOneTimeServicePaymentAdmin(admin.ModelAdmin):
    model = GuestOneTimeServicePayment
    list_display = ['service', 'guest', 'paid', 'paid_date']



admin.site.register(Service, ServiceAdmin)
admin.site.register(GuestCreatedSubscription, GuestCreatedSubscriptionAdmin)
admin.site.register(GuestOneTimeServicePayment, GuestOneTimeServicePaymentAdmin)