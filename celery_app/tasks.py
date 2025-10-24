# celery_app/tasks.py
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
from flask import Flask
from celery import group
from .celery_config import app as celery_app
from database.database import db, save_email_log

load_dotenv()

def make_flask_context():
    """
    Tạo Flask app nhỏ để Celery worker có app_context
    (dùng để SQLAlchemy hoạt động đúng trong worker).
    """
    flask_app = Flask(__name__)
    db_uri = os.getenv("DATABASE_URL", "sqlite:///email_logs.db")
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(flask_app)
    return flask_app

def send_email_smtp(to_email, subject, html_content):
    """
    Gửi email qua SMTP.
    """
    smtp_server = os.getenv("SMTP_SERVER", "smtp.gmail.com")
    smtp_port = int(os.getenv("SMTP_PORT", 587))
    smtp_user = os.getenv("SMTP_USER")          # email gửi
    smtp_pass = os.getenv("SMTP_PASS")          # app password

    if not smtp_user or not smtp_pass:
        raise ValueError("SMTP_USER và SMTP_PASS chưa được cấu hình trong .env")

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = smtp_user
    msg["To"] = to_email

    part = MIMEText(html_content, "html")
    msg.attach(part)

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(smtp_user, smtp_pass)
        server.sendmail(smtp_user, to_email, msg.as_string())

# --- Task con: gửi email 1 người ---
@celery_app.task(bind=True, name="send_single_email")
def send_single_email(self, recipient, subject, content):
    flask_app = make_flask_context()
    try:
        send_email_smtp(recipient, subject, content)
        with flask_app.app_context():
            save_email_log(recipient, subject, "Success", content)
        print(f"✅ Sent to {recipient}")
        return {"email": recipient, "status": "Success"}
    except Exception as exc:
        err = str(exc)
        with flask_app.app_context():
            save_email_log(recipient, subject, f"Error: {err}", content)
        print(f"❌ Error sending to {recipient}: {err}")
        return {"email": recipient, "status": f"Error: {err}"}

# --- Task cha: chia nhỏ ra để gửi song song ---
@celery_app.task(bind=True, name="send_bulk_emails")
def send_bulk_emails(self, subject, content, recipients):
    """
    Gửi email hàng loạt thật qua nhiều worker Celery (song song).
    """
    if not isinstance(recipients, (list, tuple)):
        raise ValueError("recipients phải là list hoặc tuple")

    # Tạo group task để chạy song song
    job_group = group(
        send_single_email.s(r, subject, content) for r in recipients
    )

    result = job_group.apply_async()  # chạy đồng thời
    results = result.get()  # chờ kết quả các worker trả về

    return {"summary": f"Processed {len(results)} emails", "details": results}
