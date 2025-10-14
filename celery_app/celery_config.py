# celery_app/celery_config.py
import os
from dotenv import load_dotenv

# Nạp biến môi trường từ file .env
load_dotenv()

# Redis broker và backend URLs
CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL", "redis://localhost:6379/0")
CELERY_RESULT_BACKEND = os.getenv("CELERY_RESULT_BACKEND", "redis://localhost:6379/1")

# Cấu hình thêm cho Celery
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'Asia/Ho_Chi_Minh'
CELERY_ENABLE_UTC = True
