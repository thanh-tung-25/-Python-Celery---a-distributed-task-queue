# celery_app/tasks.py
from .celery_config import app
from .email_utils import send_email
from db.database import save_email_log


@app.task(bind=True)
def send_bulk_emails(self, subject, content, recipients):
    """
    recipients: list of email strings
    Gửi email hàng loạt, ghi log vào SQLite.
    Trả về danh sách kết quả cho từng email.
    """
    results = []

    if not isinstance(recipients, (list, tuple)):
        raise ValueError("recipients must be a list")

    for r in recipients:
        try:
            # 📨 Gửi email
            send_email(r, subject, content)
            
            # 💾 Ghi log thành công vào SQLite
            save_email_log(
                email=r,
                subject=subject,
                body=content,
                status="success"
            )
            results.append(f"✅ Sent successfully: {r}")

        except Exception as exc:
            # 💾 Ghi log thất bại
            save_email_log(
                email=r,
                subject=subject,
                body=content,
                status=f"failed ({str(exc)})"
            )
            results.append(f"❌ Failed: {r} -> {str(exc)}")

    return results
