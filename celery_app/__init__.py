# celery_app/__init__.py
from celery import Celery
from .celery_config import CELERY_BROKER_URL, CELERY_RESULT_BACKEND

celery_app = Celery(
    "email_tasks",
    broker=CELERY_BROKER_URL,
    backend=CELERY_RESULT_BACKEND
)

celery_app.conf.update(
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    timezone="Asia/Ho_Chi_Minh",
    enable_utc=True
)
