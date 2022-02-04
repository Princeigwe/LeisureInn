from unicodedata import name
from django.urls import path
from .views import (all_services_page,
                    service_subscriptions,
                    subscription_payment_process,
                    subscription_payment_successful,
                    fetch_guest_subscriptions,
                    cancel_subscription_payment_plan,
                    one_time_service_payment_process,
                    one_time_service_payment_successful,
                    one_time_service_payment_failed,
                    one_time_services)

app_name = "hotel_services"

urlpatterns = [
    path('', all_services_page, name='all_services'),
    path('<str:service_name>/subscriptions/<int:service_id>/', service_subscriptions, name="service_subscriptions"),
    path('subscriptions/<int:subscription_id>/subscription-payment/', subscription_payment_process, name="subscription_payment_process"),
    path('subscriptions/<int:id>/subscription-payment-successful/', subscription_payment_successful, name="subscription_payment_successful"),
    path('subscriptions/fetch-subscriptions', fetch_guest_subscriptions, name="fetch_guest_subscriptions"),
    path('subscriptions/<int:id>/cancel-subscription-payment/', cancel_subscription_payment_plan, name="cancel_subscription_payment"),
    path('one-time-services/', one_time_services, name="one_time_services"),
    path('<int:service_id>/one-time-payment/', one_time_service_payment_process, name="one_time_service_payment_process"),
    path('<int:id>/one-time-payment-successful/', one_time_service_payment_successful, name="one_time_service_payment_successful"),
    path('one-time-payment-failed/', one_time_service_payment_failed, name="one_time_service_payment_failed")
]
