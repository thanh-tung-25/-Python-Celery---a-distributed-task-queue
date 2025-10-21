# db/__init__.py
from .database import db, EmailLog, save_email_log

__all__ = ["db", "EmailLog", "save_email_log"]
