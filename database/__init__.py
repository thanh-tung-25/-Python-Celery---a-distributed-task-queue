# Đánh dấu thư mục 'db' là package và khởi tạo sẵn SQLite database

from .database import (
    get_session_local,
    EmailLog,
    save_email_log,
)

# Khởi tạo database nếu chưa có
def init_db():
    with app.app_context():
        db.create_all()

__all__ = ("get_session_local", "EmailLog", "save_email_log", "init_db")