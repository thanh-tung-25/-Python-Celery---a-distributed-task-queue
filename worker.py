# worker.py
from celery_app import celery_app

if __name__ == "__main__":
    celery_app.worker_main(["worker", "--loglevel=info"])
from database.database import save_email_log, db

@celery.task
def send_email_task(to, subject, body):
    try:
        # logic gửi mail ở đây ...
        send_email_real(to, subject, body)
        save_email_log(db.session, to, subject, body, "SUCCESS")
    except Exception as e:
        save_email_log(db.session, to, subject, body, f"FAILED: {e}")
