from django.urls import path
from .views import payment_process, payment_successful, payment_failed

app_name='payments'

urlpatterns = [
    path('<int:booking_id>/', payment_process, name='process'),
    path('successful/', payment_successful, name='successful'),
    path('failed/', payment_failed, name='failed')
]