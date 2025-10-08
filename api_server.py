# api_server.py
from flask import Flask, request, jsonify
from flask_cors import CORS
from celery_app.tasks import send_email_task

app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    return jsonify({"message": "Flask + Celery Email API is running 🚀"})

@app.route("/send-email", methods=["POST"])
def send_email():
    data = request.get_json()
    to_email = data.get("to_email")
    subject = data.get("subject")
    message = data.get("message")

    task = send_email_task.delay(to_email, subject, message)
    return jsonify({"task_id": task.id, "status": "Email task queued!"})

if __name__ == "__main__":
    app.run(debug=True)
