from flask import Flask, request, jsonify
from celery_app.tasks import add
from celery.result import AsyncResult
from celery_app.worker import app as celery_app

app = Flask(__name__)

@app.route("/add", methods=["POST"])
def add_task():
    data = request.get_json()
    result = add.delay(data["a"], data["b"])
    return jsonify({"task_id": result.id})

@app.route("/result/<task_id>", methods=["GET"])
def get_result(task_id):
    res = AsyncResult(task_id, app=celery_app)
    return jsonify({"status": res.status, "result": res.result if res.successful() else None})

if __name__ == "__main__":
    app.run(debug=True)
