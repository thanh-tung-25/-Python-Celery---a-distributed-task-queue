# run_task.py
from celery_app.tasks import send_email_task

if __name__ == "__main__":
    print("📤 Gửi email giả lập...")
    task = send_email_task.delay("test@example.com", "Xin chào", "Đây là email demo.")
    print("🆔 Task ID:", task.id)
    print("⏳ Đang xử lý...")
    print("📥 Kết quả:", task.get(timeout=10))
