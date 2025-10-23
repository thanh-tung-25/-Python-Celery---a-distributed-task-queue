import os
from celery import Celery
from dotenv import load_dotenv

# ============================================
# 🔧 Load biến môi trường (.env)
# ============================================
load_dotenv()

BROKER = os.getenv("CELERY_BROKER_URL", os.getenv("REDIS_URL", "redis://localhost:6379/0"))
BACKEND = os.getenv("CELERY_RESULT_BACKEND", "redis://localhost:6379/1")

# ============================================
# 🚀 Khởi tạo Celery App
# ============================================
app = Celery("celery_app", broker=BROKER, backend=BACKEND)

# ============================================
# ⚙️ Cấu hình Celery
# ============================================
app.conf.update(
    result_expires=3600,
    accept_content=["json"],
    task_serializer="json",
    result_serializer="json",
    
    # ✅ Múi giờ chính xác cho Việt Nam
    timezone=os.getenv("TIMEZONE", "Asia/Ho_Chi_Minh"),
    enable_utc=False   # ❗ Tắt UTC để không bị lệch 7 tiếng
)

# ============================================
# 🔍 Tự động tìm tasks trong celery_app
# ============================================
app.autodiscover_tasks(["celery_app"])
