# celery_app/tasks.py
import os
import smtplib
from time import sleep
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
from flask import Flask
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

    # Gửi email
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(smtp_user, smtp_pass)
        server.sendmail(smtp_user, to_email, msg.as_string())

@celery_app.task(bind=True, name="send_bulk_emails")
def send_bulk_emails(self, subject, content, recipients):
    """
    Gửi email hàng loạt thật qua SMTP và lưu log vào database.
    """
    if not isinstance(recipients, (list, tuple)):
        raise ValueError("recipients phải là list hoặc tuple")

    flask_app = make_flask_context()
    results = []

    for r in recipients:
        try:
            # Gửi mail thật
            send_email_smtp(r, subject, content)

            # Lưu log thành công
            with flask_app.app_context():
                save_email_log(r, subject, "Success", content)

            results.append({"email": r, "status": "Success"})
            print(f"✅ Sent to {r}")
            sleep(0.5)  # tránh spam quá nhanh

        except Exception as exc:
            err = str(exc)
            with flask_app.app_context():
                save_email_log(r, subject, f"Error: {err}", content)
            results.append({"email": r, "status": f"Error: {err}"})
            print(f"❌ Error sending to {r}: {err}")

    return {"summary": f"Processed {len(recipients)}", "details": results}
