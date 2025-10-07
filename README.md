# 🧩 Python Celery — A Distributed Task Queue

## 📘 Giới thiệu
Đây là một **mô hình hệ thống phân tán (Distributed System)** sử dụng **Celery** và **Redis** để thực hiện xử lý tác vụ bất đồng bộ (asynchronous task processing).

Dự án được xây dựng phục vụ môn học **Ứng dụng phân tán**, thể hiện kiến trúc **Client – Broker – Worker**, trong đó:
- **Client (Producer)** gửi yêu cầu xử lý (task)
- **Broker (Redis)** đóng vai trò hàng đợi (queue) trung gian
- **Worker (Consumer)** nhận task và thực hiện xử lý ở tiến trình khác

---

## 🧠 Kiến trúc hệ thống

+-------------+ +-------------+ +------------------+
| run_task.py | -----> | Redis Queue | -----> | Celery Worker(s) |
| (Client) | | (Broker) | | (Consumers) |
+-------------+ +-------------+ +------------------+
-Python-Celery---a-distributed-task-queue/
│
├── celery_app/
│ ├── init.py # Khởi tạo Celery app (kết nối Redis)
│ └── tasks.py # Định nghĩa các task (ví dụ: cộng 2 số)
│
├── run_task.py # Gửi task đến hàng đợi
├── requirements.txt # Các thư viện cần thiết
└── README.md # Tài liệu mô tả (file này)

---

## 🧰 Cài đặt môi trường

### 1️⃣ Tạo môi trường ảo
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
🧩 Cấu hình Redis
Sử dụng Docker:
docker run -d --name my-redis -p 6379:6379 redis
Kiểm tra Redis đang hoạt động:
docker ps
Nếu container bị dừng:
docker start my-redis
