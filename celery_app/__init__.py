# celery_app/__init__.py
from celery import Celery
import os
from dotenv import load_dotenv

# Load biến môi trường
load_dotenv()

# Cấu hình Redis
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

# Khởi tạo Celery
celery_app = Celery(
    "email_tasks",
    broker=REDIS_URL,
    backend=REDIS_URL
)

celery_app.conf.update(
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    timezone="Asia/Ho_Chi_Minh",
    enable_utc=True,
)

# Import tasks (đặt ở cuối để tránh import vòng tròn)
from celery_app import tasks  # 👈 Dòng này cực kỳ quan trọng
