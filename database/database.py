from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Khởi tạo đối tượng SQLAlchemy (sẽ được liên kết với Flask app trong api_server.py)
db = SQLAlchemy()

class EmailLog(db.Model):
    """
    Bảng lưu lịch sử gửi email.
    """
    __tablename__ = "email_logs"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(200), nullable=False)
    subject = db.Column(db.String(200))
    body = db.Column(db.Text)
    status = db.Column(db.String(50))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<EmailLog {self.email} - {self.status}>"

def save_email_log(db_session, email, subject, body, status):
    """
    Hàm lưu một bản ghi log email vào database.
    Được gọi từ Celery task hoặc Flask API.
    """
    try:
        log = EmailLog(
            email=email,
            subject=subject,
            body=body,
            status=status,
            timestamp=datetime.utcnow()
        )
        db_session.add(log)
        db_session.commit()
        print(f"💾 Saved log for {email} ({status})")
    except Exception as e:
        db_session.rollback()
        print(f"❌ Failed to save email log: {e}")