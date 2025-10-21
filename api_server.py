# api_server.py
import os
from flask import Flask, request, jsonify, send_from_directory
from celery_app.tasks import send_bulk_emails
from celery_app.celery_config import app as celery_app
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__, static_folder="frontend", static_url_path="/")

# Route frontend
@app.route("/")
def index():
    return send_from_directory("frontend", "index.html")

@app.route("/<path:path>")
def static_files(path):
    return send_from_directory("frontend", path)

# API phù hợp với frontend (script.js)
@app.route("/send-email", methods=["POST"])
def send_email():
    data = request.get_json() or {}
    # frontend có thể gửi: { "subject", "content", "recipients" }
    subject = data.get("subject")
    content = data.get("content")
    recipients = data.get("recipients")

    # nếu frontend gửi chỉ 1 email với key 'to' (cũ), hỗ trợ chuyển đổi
    if not recipients and data.get("to"):
        recipients = [data.get("to")]

    if not subject or not content or not recipients:
        return jsonify({"error": "Missing fields (subject, content, recipients/to)"}), 400

    # Tạo task Celery
    task = send_bulk_emails.delay(subject, content, recipients)
    return jsonify({"task_id": task.id, "status": "queued"}), 202

# API lấy trạng thái task
@app.route("/result/<task_id>", methods=["GET"])
def get_result(task_id):
    result = celery_app.AsyncResult(task_id)
    payload = {
        "task_id": task_id,
        "status": result.status,
        "result": result.result if result.ready() else None,
    }
    return jsonify(payload)

if __name__ == "__main__":
    # chạy dev server
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)), debug=True)