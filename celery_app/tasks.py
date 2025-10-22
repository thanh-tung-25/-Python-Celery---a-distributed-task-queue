# celery_app/tasks.py
import os
from time import sleep
from .celery_config import app as celery_app
from database.database import db, save_email_log
from flask import Flask
from dotenv import load_dotenv

load_dotenv()

def make_flask_context():
    """
    Tạo 1 Flask app nhỏ để Celery worker có app_context
    (dùng để SQLAlchemy hoạt động đúng trong worker).
    """
    flask_app = Flask(__name__)
    # dùng DATABASE_URL nếu có, còn không dùng sqlite file mặc định
    db_uri = os.getenv("DATABASE_URL", "sqlite:///email_logs.db")
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(flask_app)
    return flask_app

@celery_app.task(bind=True, name="send_bulk_emails")
def send_bulk_emails(self, subject, content, recipients):
    """
    Gửi email hàng loạt (demo). Gọi save_email_log(email, subject, status, body).
    Không truyền db.session.
    """
    if not isinstance(recipients, (list, tuple)):
        raise ValueError("recipients must be a list")

    flask_app = make_flask_context()

    results = []
    # Mỗi lần muốn thao tác DB: dùng app_context()
    for r in recipients:
        try:
            # -------------- gửi mail ở đây (mock) ----------------
            print(f"📨 (mock) sending to {r} — subject: {subject}")
            sleep(1)   # mô phỏng thời gian gửi
            # ----------------------------------------------------

            # Ghi log thành công (không truyền db.session)
            with flask_app.app_context():
                save_email_log(r, subject, "Success", content)

            results.append({"email": r, "status": "Success"})
        except Exception as exc:
            err = str(exc)
            with flask_app.app_context():
                save_email_log(r, subject, f"Error: {err}", content)
            results.append({"email": r, "status": f"Error: {err}"})

    return {"summary": f"Processed {len(recipients)}", "details": results}
