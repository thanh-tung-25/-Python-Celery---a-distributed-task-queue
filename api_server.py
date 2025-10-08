from flask import Flask, request, jsonify
from celery_app.celery_config import celery_app
from celery_app.tasks import add, reverse_text
from celery.result import AsyncResult

app = Flask(__name__)

@app.route("/add", methods=["POST"])
def add_task():
    data = request.get_json()
    a = int(data.get("a", 0))
    b = int(data.get("b", 0))
    result = add.delay(a, b)
    return jsonify({"task_id": result.id}), 202

@app.route("/result/<task_id>", methods=["GET"])
def get_result(task_id):
    res = AsyncResult(task_id, app=celery_app)
    response = {
        "task_id": task_id,
        "status": res.status,
        "result": res.result if res.successful() else None
    }
    return jsonify(response)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
