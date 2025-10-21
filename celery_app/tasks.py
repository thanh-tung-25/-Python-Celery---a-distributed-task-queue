from celery_app.celery_config import app
from celery_app.email_utils import send_email
import redis
import os
import json
from datetime import datetime
from db.database import save_email_log_sqlite

REDIS_URL = os.getenv("REDIS_URL")
r = redis.Redis.from_url(REDIS_URL)

@app.task(bind=True, max_retries=3)
def send_email_task(self, recipient, subject, body):
    timestamp = datetime.utcnow().isoformat()
    task_id = self.request.id
    try:
        send_email(recipient, subject, body)
        status = 'SUCCESS'
    except Exception as e:
        status = 'FAILURE'
        raise self.retry(exc=e, countdown=5)

    log_entry = {
        "recipient": recipient,
        "subject": subject,
        "status": status,
        "timestamp": timestamp,
        "task_id": task_id
    }

    # Lưu Redis
    r.set(f"email:{task_id}", json.dumps(log_entry), ex=86400)

    # Lưu SQLite
    save_email_log_sqlite(log_entry)

    return status
