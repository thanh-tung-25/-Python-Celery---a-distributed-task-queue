from .celery_config import app
from .email_utils import send_email
from database.database import save_email_log, db
from flask import Flask
import os

# === Tạo Flask app nhỏ để dùng context (tránh import vòng) ===
def make_flask_context():
    flask_app = Flask(__name__)
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL", "sqlite:///email_logs.db")
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(flask_app)
    return flask_app

@app.task(bind=True)
def send_bulk_emails(self, subject, content, recipients):
    """
    Task gửi email hàng loạt + lưu log vào database.
    """
    results = []

    if not isinstance(recipients, (list, tuple)):
        raise ValueError("recipients must be a list")

    # Tạo Flask context để có thể dùng SQLAlchemy trong Celery
    flask_app = make_flask_context()

    for r in recipients:
        try:
            send_email(r, subject, content)  # Gửi email
            results.append(f"✅ OK: {r}")

            # Ghi log thành công
            with flask_app.app_context():
                save_email_log(db.session, r, subject, content, "Success")

        except Exception as exc:
            error_msg = str(exc)
            results.append(f"❌ ERR: {r} -> {error_msg}")

            # Ghi log lỗi
            with flask_app.app_context():
                save_email_log(db.session, r, subject, content, f"Error: {error_msg}")

    return results