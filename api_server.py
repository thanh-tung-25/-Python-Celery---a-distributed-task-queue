from flask import Flask, request, render_template, jsonify
from celery_app.tasks import send_email_task
from db.database import init_db
import sqlite3
import os

# Chỉ định template và static folder là frontend
app = Flask(
    __name__,
    template_folder="frontend",  # chứa index.html, dashboard.html
    static_folder="frontend"     # chứa style.css, script.js
)

DB_PATH = "emails.db"
init_db()
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/send_email', methods=['POST'])
def send_email_route():
    data = request.json
    recipient = data.get("recipient")
    subject = data.get("subject")
    body = data.get("body")
    task = send_email_task.delay(recipient, subject, body)
    return jsonify({"task_id": task.id}), 202

@app.route('/dashboard')
def dashboard():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT recipient, subject, status, timestamp FROM emails ORDER BY timestamp DESC LIMIT 50")
    logs = c.fetchall()
    conn.close()
    return render_template('dashboard.html', logs=logs)

@app.route('/dashboard/stats')
def dashboard_stats():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM emails WHERE status='SUCCESS'")
    success_count = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM emails WHERE status='FAILURE'")
    failure_count = c.fetchone()[0]
    conn.close()
    return jsonify({"success": success_count, "failure": failure_count})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)), debug=True)
