# celery_app/celery_config.py
import os
from celery import Celery
from dotenv import load_dotenv

load_dotenv()  # load .env

BROKER = os.getenv("CELERY_BROKER_URL", os.getenv("REDIS_URL", "redis://localhost:6379/0"))
BACKEND = os.getenv("CELERY_RESULT_BACKEND", "redis://localhost:6379/1")

app = Celery("celery_app", broker=BROKER, backend=BACKEND)

# basic config
app.conf.update(
    result_expires=3600,
    accept_content=["json"],
    task_serializer="json",
    result_serializer="json",
    timezone=os.getenv("TIMEZONE", "UTC"),
    enable_utc=True
)

# autodiscover tasks in celery_app package
app.autodiscover_tasks(["celery_app"])