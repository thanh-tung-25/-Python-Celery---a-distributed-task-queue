from celery import Celery

# Khởi tạo app Celery
app = Celery(
    'tasks',
    broker='redis://localhost:6379/0',   # Redis làm message broker
    backend='redis://localhost:6379/0'   # Redis để lưu kết quả
)

@app.task
def add(x, y):
    return x + y

@app.task
def reverse_text(s):
    return s[::-1]

@app.task
def long_task(n):
    import time
    time.sleep(n)
    return f"Task finished after {n} seconds"
