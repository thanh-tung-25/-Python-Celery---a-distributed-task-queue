# db/database.py
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# 🧱 Tạo đối tượng SQLAlchemy (sẽ gắn với Flask app ở api_server.py)
db = SQLAlchemy()

class EmailLog(db.Model):
    """
    Bảng lưu lịch sử gửi email
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

def init_db(app):
    """
    Khởi tạo database với Flask app.
    Gọi hàm này trong api_server.py sau khi tạo app Flask.
    """
    db.init_app(app)
    with app.app_context():
        db.create_all()
        print("✅ SQLite database initialized (emails.db created).")

def save_email_log(email, subject, body, status):
    """
    Lưu một bản ghi log email vào database.
    Có thể gọi từ Flask hoặc Celery task.
    """
    try:
        log = EmailLog(
            email=email,
            subject=subject,
            body=body,
            status=status,
            timestamp=datetime.utcnow()
        )
        db.session.add(log)
        db.session.commit()
        print(f"💾 Saved log for {email} ({status})")
    except Exception as e:
        db.session.rollback()
        print(f"❌ Failed to save email log: {e}")
