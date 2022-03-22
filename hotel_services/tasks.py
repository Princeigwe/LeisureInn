from celery import Celery
from .models import GuestCreatedSubscription, GuestOneTimeServicePayment
from django.core.mail import send_mail

import requests
from requests.adapters import HTTPAdapter
from requests.exceptions import ConnectionError

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


@app.task  # this is a celery task
def subscription_payment_API_call(request):

    amount = request.session['amount']
    name = request.session['name']
    interval = request.session['interval']
    seckey = request.session['seckey']

    flutterwave_adapter = HTTPAdapter(max_retries=5)
    session = requests.Session()

    session.mount("https://api.ravepay.co/v2/gpx/paymentplans/create", flutterwave_adapter)
    url = "https://api.ravepay.co/v2/gpx/paymentplans/create" ## payment plan endpoint
    payload = dict(amount=amount, name=name, interval=interval, seckey=seckey)

    try:
        subscription_post_request= session.post(url=url, json=payload)
        print(subscription_post_request.text)
    except ConnectionError as ce:
        print(ce)
    
    request.session['subscription_post_request_response'] = subscription_post_request.json()