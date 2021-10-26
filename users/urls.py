from django.urls import path
from .views import update_user_detail

app_name='users'

urlpatterns = [
    path('profile-update/', update_user_detail, name='profile-update')
]