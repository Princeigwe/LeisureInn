from celery import Celery, shared_task
from .models import GuestCreatedSubscription, GuestOneTimeServicePayment
from django.core.mail import send_mail

import requests
from requests.adapters import HTTPAdapter
from requests.exceptions import ConnectionError

# setting up the celery app
app = Celery(app="LeisureInn", broker="amqps://drzmfmjq:zKOJkSm-OZo7Obpd1q_ulUz4APdmXop7@fox.rmq.cloudamqp.com/drzmfmjq")

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


@shared_task ## shared_task decorator helps you use the return value in the views.py, as long as a result backend is provided.
def subscription_payment_API_call(amount, name, interval, seckey):

    flutterwave_adapter = HTTPAdapter(max_retries=5)
    session = requests.Session()

    session.mount("https://api.ravepay.co/v2/gpx/paymentplans/create", flutterwave_adapter)
    url = "https://api.ravepay.co/v2/gpx/paymentplans/create" ## payment plan endpoint
    payload = dict(amount=amount, name=name, interval=interval, seckey=seckey)

    try:
        subscription_post_request= session.post(url=url, json=payload) # making a POST request to the url with the payload
        print(subscription_post_request.text)
    except ConnectionError as ce:
        print(ce)
    
    return subscription_post_request.json() ## returning json response


@app.task  # this is a celery task
def cancel_subscription_payment_API_call(payment_id, seckey):
    flutterwave_cancel_payment_adapter = HTTPAdapter(max_retries=5)
    session = requests.Session()
    session.mount("https://api.ravepay.co/v2/gpx/paymentplans/{id}/cancel", flutterwave_cancel_payment_adapter)

    url = "https://api.ravepay.co/v2/gpx/paymentplans/{id}/cancel".format(id=payment_id)
    
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }
    
    payload = dict(seckey=seckey)
    try:
        subscription_cancel_request= session.post(url=url, json=payload, headers=headers)
        print(subscription_cancel_request.text)
    except ConnectionError as ce:
        print(ce)
