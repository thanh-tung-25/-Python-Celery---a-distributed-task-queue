# Đánh dấu thư mục 'db' là package và khởi tạo sẵn SQLite database

from .database import (
    Base,
    engine,
    SessionLocal,
    EmailLog,
    save_email_log,
    init_db,
)

# Khởi tạo database nếu chưa có
init_db()

__all__ = ("Base", "engine", "SessionLocal", "EmailLog", "save_email_log", "init_db")
