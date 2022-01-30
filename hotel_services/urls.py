from django.urls import path
from .views import all_services_page, service_subscriptions, subscription_payment_process, subscription_payment_successful

app_name = "hotel_services"

urlpatterns = [
    path('', all_services_page, name='all_services'),
    path('<str:service_name>/subscriptions/<int:service_id>/', service_subscriptions, name="service_subscriptions"),
    path('subscriptions/<int:subscription_id>/subscription-payment/', subscription_payment_process, name="subscription_payment_process"),
    path('subscriptions/subscription-payment-successful/', subscription_payment_successful, name="subscription_payment_successful")
]
