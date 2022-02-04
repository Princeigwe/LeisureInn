from datetime import datetime
from pyexpat import model
from django.db import models
from django.contrib.auth import get_user_model
from django.utils.timezone import now

# Create your models here.

User = get_user_model()

SUBSCRIPTION_PLAN = (
    ('STANDARD',"standard"),
    ('MASTER',"master"),
    ('PREMIUM',"premium"),
)

class Service(models.Model):
    name = models.CharField(max_length=50)
    image = models.ImageField(upload_to='hotel_services/')
    description = models.TextField()
    
    def __str__(self):
        return self.name


# add day field to subscription model
class Subscription(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="hotel_services/", default='')
    plan = models.CharField(max_length=50, choices=SUBSCRIPTION_PLAN)
    days = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=50, default='')
    
    def __str__(self):
        return str(self.service.name)


class GuestCreatedSubscription(models.Model):
    subscription = models.ForeignKey(Subscription, on_delete=models.SET_NULL, null=True)
    guest = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    cancelled = models.BooleanField(default=False)
    date_created = models.DateTimeField(default=now)
    date_cancelled = models.DateTimeField(blank=True)
    payment_id = models.IntegerField(default=0)
    
    def __str__(self):
        return str(self.subscription.service.name)


class OneTimeService(models.Model):
    service = models.OneToOneField(Service, on_delete=models.CASCADE, related_name='one_time_service')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return str(self.service)


class GuestOneTimeServicePayment(models.Model):
    service = models.ForeignKey(OneTimeService, on_delete=models.SET_NULL, null=True)
    guest = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    paid = models.BooleanField(default=True)
    paid_date = models.DateTimeField(default=now)
    
    def __str__(self):
        return str(self.service.name)
