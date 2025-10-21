# api_server.py
import os
from flask import Flask, request, jsonify, send_from_directory
from celery_app.tasks import send_bulk_emails
from celery_app.celery_config import app as celery_app
from dotenv import load_dotenv

# --- Thêm phần DB ---
from db.database import db, EmailLog

load_dotenv()

# ---------------------
# Cấu hình Flask app
# ---------------------
app = Flask(__name__, static_folder="frontend", static_url_path="/")

# Cấu hình SQLite
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///emails.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Khởi tạo DB
db.init_app(app)
with app.app_context():
    db.create_all()

# ---------------------
# Route frontend
# ---------------------
@app.route("/")
def index():
    return send_from_directory("frontend", "index.html")

@app.route("/<path:path>")
def static_files(path):
    return send_from_directory("frontend", path)

# ---------------------
# API gửi email
# ---------------------
@app.route("/send-email", methods=["POST"])
def send_email():
    data = request.get_json() or {}

    subject = data.get("subject")
    content = data.get("content")
    recipients = data.get("recipients")

    # hỗ trợ backward compatibility
    if not recipients and data.get("to"):
        recipients = [data.get("to")]

    if not subject or not content or not recipients:
        return jsonify({"error": "Missing fields (subject, content, recipients/to)"}), 400

    # Gửi email qua Celery
    task = send_bulk_emails.delay(subject, content, recipients)
    return jsonify({"task_id": task.id, "status": "queued"}), 202


# ---------------------
# API kiểm tra trạng thái task
# ---------------------
@app.route("/result/<task_id>", methods=["GET"])
def get_result(task_id):
    result = celery_app.AsyncResult(task_id)
    payload = {
        "task_id": task_id,
        "status": result.status,
        "result": result.result if result.ready() else None,
    }
    return jsonify(payload)


# ---------------------
# API xem lịch sử email (log)
# ---------------------
@app.route("/logs", methods=["GET"])
def get_email_logs():
    """
    API trả về danh sách log email đã gửi.
    Có thể lọc theo ?status=success hoặc ?status=failed.
    """
    status_filter = request.args.get("status")

    query = EmailLog.query
    if status_filter:
        query = query.filter(EmailLog.status.contains(status_filter))

    logs = query.order_by(EmailLog.timestamp.desc()).all()

    data = [
        {
            "id": log.id,
            "email": log.email,
            "subject": log.subject,
            "status": log.status,
            "timestamp": log.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
        }
        for log in logs
    ]
    return jsonify(data)


# ---------------------
# Main run
# ---------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)), debug=True)
