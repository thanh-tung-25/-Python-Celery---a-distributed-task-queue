# celery_app/tasks.py
from .celery_config import app
from .email_utils import send_email
from db import save_email_log
@app.task(bind=True)
def send_bulk_emails(self, subject, content, recipients):
    """
    recipients: list of email strings
    Trả về list kết quả (string) hoặc raise lỗi.
    """
    results = []
    if not isinstance(recipients, (list, tuple)):
        raise ValueError("recipients must be a list")

    for r in recipients:
        try:
            send_email(r, subject, content)
            results.append(f"OK: {r}")
        except Exception as exc:
            # ghi lỗi vào result và tiếp tục gửi cho các email khác
            results.append(f"ERR: {r} -> {str(exc)}")
    return results
