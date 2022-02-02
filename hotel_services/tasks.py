from celery import Celery, app #app is a decorator
from .models import GuestCreatedSubscription
from django.core.mail import send_mail

# setting up the celery app
app = Celery(app="LeisureInn", broker="amqp://guest:guest@rabbitmq:5672/")

@app.task
def service_subscription_confirmation_email(guestCreatedSubscription_id):
    guestCreatedSubscription = GuestCreatedSubscription.objects.get(id=guestCreatedSubscription_id)
    subject = "Subscription Payment Plan Created"
    message = f'We are notifying you that a user with this email:{guestCreatedSubscription.guest.email}, successfully created a subscription payment plan for {guestCreatedSubscription.subscription} {guestCreatedSubscription.subscription.plan} plan'
    send_mail(subject, message, "admin@leisureinn@gmail.com", [guestCreatedSubscription.guest.email], fail_silently=False)