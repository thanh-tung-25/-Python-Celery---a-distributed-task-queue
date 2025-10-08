# celery_app/tasks.py
from . import celery_app
import time

@celery_app.task(bind=True)
def send_email_task(self, to_email, subject, message):
    """
    Task giả lập gửi email bất đồng bộ
    """
    try:
        print("📧 [TASK START] Bắt đầu gửi email...")
        time.sleep(3)
        print("----------------------------------------------------")
        print(f"TO: {to_email}")
        print(f"SUBJECT: {subject}")
        print(f"MESSAGE: {message}")
        print("----------------------------------------------------")
        print("✅ [TASK DONE] Email giả lập đã gửi xong!")
        return f"[SIMULATED] Email sent to {to_email}"
    except Exception as e:
        print(f"❌ Lỗi task: {e}")
        raise self.retry(exc=e, countdown=10, max_retries=3)
