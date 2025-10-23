# worker.py
import subprocess
import time

workers = ["worker1", "worker2", "worker3"]

for name in workers:
    print(f"🚀 Starting {name} ...")
    subprocess.Popen(
        [
            "venv\\Scripts\\celery",
            "-A", "celery_app.celery_config.app",
            "worker",
            "--loglevel=info",
            "-P", "solo",
            "-n", f"{name}@%h"
        ],
        creationflags=subprocess.CREATE_NEW_CONSOLE
    )
    time.sleep(1)

print("✅ Đã khởi động 3 Celery workers thành công!")
input("Nhấn Enter để dừng...")
