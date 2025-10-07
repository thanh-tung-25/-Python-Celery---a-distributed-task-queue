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