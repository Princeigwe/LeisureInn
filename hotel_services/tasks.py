from celery import Celery
from .models import GuestCreatedSubscription, GuestOneTimeServicePayment
from django.core.mail import send_mail

# setting up the celery app
app = Celery(app="LeisureInn", broker="amqp://guest:guest@rabbitmq:5672/")

@app.task # this is a celery task
def service_subscription_confirmation_email(guestCreatedSubscription_id):
    guestCreatedSubscription = GuestCreatedSubscription.objects.get(id=guestCreatedSubscription_id)
    subject = "Subscription Payment Plan Created"
    message = f'We are notifying you that a user with this email:{guestCreatedSubscription.guest.email}, successfully created a subscription payment plan for {guestCreatedSubscription.subscription} {guestCreatedSubscription.subscription.plan} plan'
    send_mail(subject, message, "admin@leisureinn@gmail.com", [guestCreatedSubscription.guest.email], fail_silently=False)


@app.task  # this is a celery task
def one_time_payment_confirmation_email(id):
    guestOneTimeServicePayment = GuestOneTimeServicePayment.objects.get(id=id)
    subject = "Subscription Payment Plan Created"
    message = f'We are notifying you that a user with this email:{guestOneTimeServicePayment.guest.email}, successfully paid for {guestOneTimeServicePayment.service}  for NGN{guestOneTimeServicePayment.service.price}'
    send_mail(subject, message, "admin@leisureinn@gmail.com", [guestOneTimeServicePayment.guest.email], fail_silently=False)
