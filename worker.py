from celery_app.celery_config import celery_app

if __name__ == "__main__":
    # Chạy worker trực tiếp (tùy chọn)
    celery_app.worker_main(argv=["worker", "--loglevel=info", "--pool=solo"])
