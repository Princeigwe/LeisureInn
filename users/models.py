from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
from .managers import CustomUserManager
from bookings.models import Booking
# Create your models here.
from datetime import date
from django.utils import timezone


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique=True)
    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    age = models.PositiveSmallIntegerField()
    image = models.ImageField(upload_to='profile_pictures/', blank=True)
    country = models.CharField(max_length=100, blank=True)
    occupation = models.CharField(max_length=100, blank=True)
    birthday = models.DateField(auto_now=False, blank=True, default=timezone.now)
    mobile = models.CharField(max_length=12, blank=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    objects = CustomUserManager()
    
    def __str__(self):
        return self.email


