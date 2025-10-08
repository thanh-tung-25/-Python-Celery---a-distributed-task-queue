from .celery_config import celery_app

@celery_app.task(name="celery_app.tasks.add")
def add(x, y):
    """Ví dụ task: cộng hai số"""
    return x + y

@celery_app.task(name="celery_app.tasks.reverse_text")
def reverse_text(s: str):
    return s[::-1]
