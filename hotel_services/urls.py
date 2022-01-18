from django.urls import path
from .views import all_services_page, service_subscriptions

app_name = "hotel_services"

urlpatterns = [
    path('', all_services_page, name='all_services'),
    path('<str:service_name>/subscriptions/<int:service_id>/', service_subscriptions, name="service_subscriptions")
]
