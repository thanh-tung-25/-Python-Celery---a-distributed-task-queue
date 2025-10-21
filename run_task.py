# run_task.py
from celery_app.tasks import send_bulk_emails

if __name__ == "__main__":
    recipients = [
        "recipient1@example.com",
        # thêm email thực để test
    ]
    res = send_bulk_emails.delay("Test subject from Celery", "<h3>Test content</h3>", recipients)
    print("Task queued:", res.id)