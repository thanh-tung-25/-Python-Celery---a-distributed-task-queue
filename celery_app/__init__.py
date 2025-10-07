from celery import Celery

app = Celery(
    "celery_app",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0"
)

# Tự động load tasks từ module celery_app.tasks
app.autodiscover_tasks(["celery_app"])
