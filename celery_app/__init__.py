import os
import sys

# 🧩 Thêm đường dẫn project gốc để Celery có thể import được các module như 'database'
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from .celery_config import app

__all__ = ("app",)