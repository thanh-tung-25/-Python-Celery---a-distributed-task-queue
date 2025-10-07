# 🧩 Python Celery — A Distributed Task Queue

## 📘 Giới thiệu
Đây là một **mô hình hệ thống phân tán (Distributed System)** sử dụng **Celery** và **Redis** để thực hiện xử lý tác vụ bất đồng bộ (asynchronous task processing).

Dự án được xây dựng phục vụ môn học **Ứng dụng phân tán**, thể hiện kiến trúc **Client – Broker – Worker**, trong đó:
- **Client (Producer)** gửi yêu cầu xử lý (task)
- **Broker (Redis)** đóng vai trò hàng đợi (queue) trung gian
- **Worker (Consumer)** nhận task và thực hiện xử lý ở tiến trình khác

---

## 🧠 Kiến trúc hệ thống

+-------------+ +-----------------------------+ +----------------+
| run_task.py | -----> | Redis Queue | -----> | Celery Worker(s) |
|   (Client)  |        |  (Broker)   |        |  (Consumers)     |
+-------------+ +-----------------------------+ +----------------+
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
🚀 Chạy hệ thống
Mở Cửa sổ 1 – Worker
cd C:\xampp\htdocs\-Python-Celery---a-distributed-task-queue
.\venv\Scripts\Activate.ps1
celery -A celery_app worker --loglevel=info --pool=solo
Mở Cửa sổ 2 – Client
cd C:\xampp\htdocs\-Python-Celery---a-distributed-task-queue
.\venv\Scripts\Activate.ps1
python run_task.py
Kết quả:
📤 Đã gửi task cộng 10 + 20
📥 Kết quả: 30
📄 Mô tả kỹ thuật
| Thành phần               | Vai trò                       | Công nghệ    |
| ------------------------ | ----------------------------- | ------------ |
| `run_task.py`            | Gửi task đến Redis (Producer) | Python       |
| `Redis`                  | Message Broker + Backend      | Docker Redis |
| `celery_app/__init__.py` | Khởi tạo Celery App           | Celery       |
| `celery_app/tasks.py`    | Định nghĩa task thực thi      | Celery Task  |
| `celery worker`          | Nhận và xử lý task (Consumer) | Celery       |
🧠 Kết luận

Dự án minh họa mô hình phân tán tác vụ (Distributed Task Queue) với:

Tính bất đồng bộ (asynchronous)

Phân tán xử lý giữa nhiều tiến trình / máy

Mở rộng dễ dàng bằng việc thêm worker mới

Celery + Redis là một giải pháp phổ biến trong các hệ thống phân tán thực tế như:

Gửi email hàng loạt

Xử lý dữ liệu lớn (batch processing)

Lên lịch tác vụ định kỳ

Xử lý nền trong web application

👨‍💻 Tác giả
Đặng Thanh Tùng 
Lê Đình Đức Anh

📚 Tham khảo
Celery Documentation
Redis Documentation
Python Official Website
