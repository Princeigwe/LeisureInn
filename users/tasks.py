from celery import Celery, app
from django.core.mail import send_mail

app = Celery(app="LeisureInn", broker="amqp://guest:guest@rabbitmq:5672/")

import requests

@app.task
def send_user_email(subject, message, sender, recipient):
    """the backgorund task for sending user email in the user bio data page"""
    send_mail(subject, message, sender, [recipient], fail_silently=False)