import os

from celery import Celery

#  setting environvariable for celery to find django project (LeisureInn)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "LeisureInn.settings")

app = Celery("LeisureInn")  # creating a celery instance and assigning it to "app" variable
app.conf.update(BROKER_URL=os.environ['CLOUDAMQP_URL'],
                CELERY_RESULT_BACKEND='rpc://',
                CELERY_BROKER_POOL_LIMIT = 1,
                CELERY_RESULT_PERSISTENT = True,
                )
app.config_from_object("django.conf:settings", namespace="CELERY") # loading celery configuration values from django.conf settings
app.autodiscover_tasks() # telling celery to autodiscover tasks
