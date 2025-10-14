from celery import Celery
import os
from dotenv import load_dotenv

# Tải biến môi trường từ file .env
load_dotenv()

# Đọc URL Redis từ biến môi trường hoặc dùng mặc định
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

# Tạo đối tượng Celery
celery_app = Celery(
    "celery_tasks",
    broker=REDIS_URL,          # Redis làm broker
    backend=REDIS_URL          # Redis cũng làm backend lưu kết quả
)

# Cấu hình Celery (tùy chọn)
celery_app.conf.update(
    result_expires=3600,        # Task hết hạn sau 1h
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"]
)

@celery_app.task
def add(x, y):
    """Ví dụ 1 task đơn giản"""
    return x + y
