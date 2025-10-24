import os
from flask import Flask, request, jsonify, send_from_directory
from celery_app.tasks import send_bulk_emails
from celery_app.celery_config import app as celery_app
from dotenv import load_dotenv
from database.database import db, save_email_log, EmailLog
from datetime import datetime
import pytz

# ============================================
# 🔧 Load biến môi trường (.env)
# ============================================
load_dotenv()

# ============================================
# 🚀 Khởi tạo Flask App
# ============================================
app = Flask(__name__, static_folder="frontend", static_url_path="/")

# ============================================
# ⚙️ Cấu hình Database
# ============================================
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL", "sqlite:///email_logs.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["TIMEZONE"] = os.getenv("TIMEZONE", "Asia/Ho_Chi_Minh")

# Gắn SQLAlchemy vào Flask app
db.init_app(app)

# ============================================
# 🌐 ROUTES FRONTEND
# ============================================
@app.route("/")
def index():
    return send_from_directory("frontend", "index.html")

@app.route("/<path:path>")
def static_files(path):
    return send_from_directory("frontend", path)

# ============================================
# 📤 API GỬI EMAIL (qua Celery task)
# ============================================
@app.route("/send-email", methods=["POST"])
def send_email():
    data = request.get_json() or {}
    subject = data.get("subject")
    content = data.get("content")
    recipients = data.get("recipients")

    # hỗ trợ key cũ 'to'
    if not recipients and data.get("to"):
        recipients = [data.get("to")]

    if not subject or not content or not recipients:
        return jsonify({"error": "Missing fields (subject, content, recipients/to)"}), 400

    task = send_bulk_emails.delay(subject, content, recipients)
    return jsonify({"task_id": task.id, "status": "queued"}), 202

# ============================================
# 📊 API XEM TRẠNG THÁI TASK
# ============================================
@app.route("/result/<task_id>", methods=["GET"])
def get_result(task_id):
    result = celery_app.AsyncResult(task_id)
    payload = {
        "task_id": task_id,
        "status": result.status,
        "result": result.result if result.ready() else None,
    }
    return jsonify(payload)

# ============================================
# 🧾 API XEM LỊCH SỬ GỬI EMAIL (LOG)
# ============================================
@app.route("/logs", methods=["GET"])
def get_logs():
    logs = EmailLog.query.order_by(EmailLog.timestamp.desc()).all()
    tz = pytz.timezone(app.config["TIMEZONE"])
    return jsonify([
        {
            "id": log.id,
            "email": log.email,
            "subject": log.subject,
            "status": log.status,
            # ✅ Hiển thị đúng giờ Việt Nam
            "timestamp": log.timestamp.astimezone(tz).strftime("%Y-%m-%d %H:%M:%S")
        } for log in logs
    ])

# ============================================
# ▶️ KHỞI CHẠY FLASK APP
# ============================================
if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(
        host="0.0.0.0",
        port=int(os.getenv("PORT", 5000)),
        debug=True
    )
