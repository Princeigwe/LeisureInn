from celery import Celery
from django.core.mail import send_mail

# app = Celery(app="LeisureInn", broker="amqp://guest:guest@rabbitmq:5672/") # app is the name of the project, broker is the url of the message broker
app = Celery(app="LeisureInn", broker="amqps://drzmfmjq:zKOJkSm-OZo7Obpd1q_ulUz4APdmXop7@fox.rmq.cloudamqp.com/drzmfmjq")

@app.task # this is a celery task
def send_user_email(subject, message, sender, recipient):
    """the backgorund task for sending user email in the user bio data page"""
    send_mail(subject, message, sender, [recipient], fail_silently=False)