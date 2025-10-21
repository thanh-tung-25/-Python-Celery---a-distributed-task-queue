import os
from celery import Celery
from dotenv import load_dotenv

load_dotenv()

CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL")
CELERY_RESULT_BACKEND = os.getenv("CELERY_RESULT_BACKEND")
TIMEZONE = os.getenv("TIMEZONE", "UTC")

app = Celery('email_sender', broker=CELERY_BROKER_URL, backend=CELERY_RESULT_BACKEND)
app.conf.timezone = TIMEZONE
app.conf.task_routes = {'celery_app.tasks.*': {'queue': 'email_queue'}}
