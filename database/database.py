from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy.orm import sessionmaker
import os

# Khởi tạo Flask app tạm để tạo DB
app = Flask(__name__)

# Đường dẫn DB (sqlite nằm ngay thư mục gốc dự án)
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DB_PATH = os.path.join(BASE_DIR, "..", "email_logs.db")

app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DB_PATH}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Khởi tạo SQLAlchemy
db = SQLAlchemy(app)

# ==============================
# Định nghĩa SessionLocal trong ngữ cảnh ứng dụng
# ==============================
def get_session_local():
    return sessionmaker(autocommit=False, autoflush=False, bind=db.engine)

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
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<EmailLog {self.email} - {self.status}>"

# ==============================
# Hàm lưu log
# ==============================
def save_email_log(db_session, email, subject, body, status):
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

# ==============================
# Tạo database nếu chạy trực tiếp
# ==============================
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        print("✅ Database 'email_logs.db' created successfully!")