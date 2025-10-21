# celery_worker.py
# (Chỉ cần khi bạn muốn chạy worker bằng `python celery_worker.py` - nhưng
#  thường khuyên dùng lệnh celery CLI)
from celery_app.celery_config import app

if __name__ == "__main__":
    # khởi tạo worker qua app.start (không phổ biến, CLI tốt hơn)
    app.start()