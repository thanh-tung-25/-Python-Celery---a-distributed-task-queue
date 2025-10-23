from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import pytz

# Khởi tạo SQLAlchemy (chưa gắn app, sẽ gắn trong api_server.py)
db = SQLAlchemy()

# ==============================
# Model: EmailLog
# ==============================
class EmailLog(db.Model):
    __tablename__ = "email_logs"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(200), nullable=False)
    subject = db.Column(db.String(200))
    body = db.Column(db.Text)
    status = db.Column(db.String(50))
    # ✅ dùng giờ Việt Nam thay vì UTC
    timestamp = db.Column(
        db.DateTime,
        default=lambda: datetime.now(pytz.timezone("Asia/Ho_Chi_Minh"))
    )

    def __repr__(self):
        return f"<EmailLog {self.email} - {self.status}>"

# ==============================
# Hàm lưu log (dùng chung cho Flask & Celery)
# ==============================
def save_email_log(email, subject, status, body=None):
    """Lưu log email vào database"""
    try:
        log = EmailLog(email=email, subject=subject, body=body, status=status)
        db.session.add(log)
        db.session.commit()
        print(f"💾 Saved log for {email} ({status})")
    except Exception as e:
        db.session.rollback()
        print(f"❌ Failed to save email log: {e}")
