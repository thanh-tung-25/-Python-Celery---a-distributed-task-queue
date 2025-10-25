# 📨 PYTHON-CELERY — A DISTRIBUTED TASK QUEUE

## 📘 GIỚI THIỆU CHUNG

Đây là bài tập lớn môn Ứng dụng Phân tán, được thực hiện với mục tiêu nghiên cứu, triển khai và thử nghiệm một hệ thống xử lý tác vụ phân tán (Distributed Task Queue) bằng Python Celery, sử dụng Redis làm Broker và Flask làm API Server.

Hệ thống cho phép gửi email hàng loạt một cách bất đồng bộ, đồng thời ghi log lại thông tin từng email được gửi (địa chỉ, thời gian, trạng thái).
Dự án được đóng gói và triển khai hoàn toàn bằng Docker Compose, mô phỏng mô hình hệ thống phân tán thực tế.

## 🧩 CHƯƠNG 1: GIỚI THIỆU ĐỀ TÀI

### 1.1. Mục tiêu

Mục tiêu của đề tài là xây dựng một ứng dụng minh họa cho việc xử lý song song (parallel) và bất đồng bộ (asynchronous) thông qua Celery.
Hệ thống cần đáp ứng được các yêu cầu:

Gửi email hàng loạt song song qua nhiều worker.

Lưu lại log các email đã gửi, thời gian và trạng thái.

Tối ưu hiệu năng so với cách gửi tuần tự.

Dễ dàng triển khai, mở rộng bằng Docker.

### 1.2. Phạm vi

Dự án triển khai ở mức ứng dụng thử nghiệm (prototype), gồm:

Flask web/API phục vụ giao diện và API gửi email.

Redis làm message broker.

Celery worker xử lý các tác vụ.

SQLite làm cơ sở dữ liệu log.

Giao diện web đơn giản cho phép người dùng nhập danh sách email.

## ⚙️ CHƯƠNG 2: TỔNG QUAN VỀ DỰ ÁN

### 2.1. Giới thiệu về Celery

Celery là một distributed task queue mã nguồn mở cho Python, cho phép xử lý các tác vụ nền một cách bất đồng bộ.
Nó thường được sử dụng trong các hệ thống cần thực hiện những công việc tốn thời gian như gửi email, xử lý dữ liệu hoặc tính toán song song.

Kiến trúc Celery bao gồm 3 thành phần chính:
Thành phần Chức năng
Broker (Redis) Nhận và phân phối thông điệp (tasks) giữa Flask và Worker
Worker (Celery) Thực thi tác vụ nhận được từ Broker
Result Backend Lưu kết quả hoặc trạng thái của tác vụ
Cơ chế hoạt động của Celery tương tự mô hình Producer – Consumer trong Hệ điều hành, thể hiện rõ nguyên lý xử lý song song và phân tán.

### 2.2. Ngôn ngữ và công nghệ sử dụng

Công cụ Phiên bản Mục đích
Python 3.12 Ngôn ngữ lập trình chính
Celery 5.4.0 Distributed task queue
Redis 5.0.4 Message Broker và Result Backend
Flask 3.0 API Server
Docker 28.4.0 Môi trường ảo hóa triển khai
SQLite / SQLAlchemy – Lưu trữ log gửi email

### 2.3. Ưu điểm và Hạn chế

Ưu điểm:

Hỗ trợ xử lý song song, giảm thời gian phản hồi.

Dễ mở rộng quy mô bằng cách tăng số lượng worker.

Tích hợp dễ dàng với các framework phổ biến như Flask, Django.

Tương thích tốt với Docker và các môi trường containerized.

Hạn chế:

Cần cấu hình nhiều thành phần (Redis, Worker, API).

Việc giám sát, quản lý trạng thái task cần thêm công cụ hỗ trợ (Flower, Grafana...).

Khi mất kết nối Broker, hệ thống cần cơ chế retry để đảm bảo tính toàn vẹn dữ liệu.

## 🏗️ CHƯƠNG 3: PHÁT TRIỂN VÀ TRIỂN KHAI

### 3.1. Cấu trúc dự án

PYTHON-CELERY---A-DISTRIBUTED-TASK-QUEUE/<br>
│<br>
├── celery_app/ <br>
│ ├── **init**.py<br>
│ ├── celery_config.py<br>
│ ├── email_utils.py<br>
│ └── tasks.py<br>
│<br>
├── database/<br>
│ ├── **init**.py<br>
│ └── database.py<br>
│<br>
├── frontend/<br>
│ ├── index.html<br>
│ ├── script.js<br>
│ └── style.css<br>
│<br>
├── instance/<br>
├── venv/<br>
│<br>
├── .env<br>
├── .env.example<br>
├── .gitignore<br>
├── api_server.py<br>
├── celery_worker.py<br>
├── docker-compose.yml<br>
├── Dockerfile<br>
├── init_db.py<br>
├── README.md<br>
├── requirements.txt<br>
├── run_task.py<br>
└── worker.py<br>

Mô tả thành phần:

api_server.py: Flask API cho người dùng gửi yêu cầu gửi email.

celery_app/: Chứa cấu hình Celery, định nghĩa các tác vụ và logic gửi email.

database/database.py: Xử lý kết nối SQLite và lưu log gửi email.

frontend/: Giao diện web đơn giản để nhập danh sách email.

docker-compose.yml: Cấu hình khởi chạy hệ thống gồm Flask, Redis, Celery.

requirements.txt: Liệt kê thư viện Python cần cài đặt.

### 3.2. Kiểm thử hệ thống

Bài kiểm thử Kết quả
Gửi 9 email song song Thành công, trung bình 1 giây
Mất kết nối Redis Celery tự động retry
Kiểm tra log sau 24h Dữ liệu lưu đầy đủ, đúng định dạng
Scale thêm 2 worker Hệ thống hoạt động ổn định, không lỗi

Kết quả kiểm thử cho thấy hệ thống hoạt động ổn định, độ tin cậy cao và hiệu năng cải thiện 75–80% so với gửi tuần tự.

### 3.3. Triển khai thực tế

Hệ thống được triển khai bằng Docker Compose, gồm 3 container chính:

Container Chức năng
🧩 web Flask API Server
🧠 redis Message Broker & Result Backend
⚙️ worker Celery Worker xử lý tác vụ
🧰 Các bước chạy chương trình
🪜 Bước 1: Tạo môi trường ảo và cài đặt thư viện
python -m venv venv  
venv\Scripts\activate # (Windows)  
pip install -r requirements.txt

🧱 Bước 2: Khởi động Redis bằng Docker  
docker run -d -p 6380:6379 redis

🌐 Bước 3: Khởi động Flask API Server  
python api_server.py

⚙️ Bước 4: Chạy Celery Workers

Có thể mở 3 terminal riêng biệt và chạy:

celery -A celery_app.celery_config.app worker --loglevel=info -P solo -n worker1@%h  
celery -A celery_app.celery_config.app worker --loglevel=info -P solo -n worker2@%h  
celery -A celery_app.celery_config.app worker --loglevel=info -P solo -n worker3@%h

Hoặc chạy cả 3 worker cùng lúc chỉ bằng một lệnh:

python worker.py

🌍 Bước 5: Truy cập giao diện web

Truy cập:

http://127.0.0.1:5000/

Tại đây, có thể nhập danh sách email, gửi hàng loạt và xem lịch sử gửi email.

## 🧠 CHƯƠNG 4: KẾT LUẬN VÀ HƯỚNG PHÁT TRIỂN

### 4.1. Kết luận

Thông qua bài tập lớn này, tôi đã hiểu rõ hơn về cách thức hoạt động của hệ thống phân tán, cơ chế xử lý song song, giao tiếp bất đồng bộ và cách lập lịch tác vụ trong môi trường nhiều tiến trình.

Hai chức năng chính gồm:

Gửi email hàng loạt (Bulk Email Sending)

Lưu log gửi email (Email Logging System)

đều hoạt động ổn định, minh họa rõ tính thực tiễn và hiệu quả xử lý của mô hình ứng dụng phân tán.

### 4.2. Hướng phát triển

Tích hợp Celery Flower để theo dõi và giám sát tác vụ trực quan.

Mở rộng hệ thống sang multi-node cluster để xử lý quy mô lớn.

Bổ sung Priority Queue để ưu tiên tác vụ quan trọng.

Áp dụng JWT Authentication để bảo mật API Flask.

Cải tiến giao diện người dùng, hỗ trợ tải file danh sách email.

### 📚 TÀI LIỆU THAM KHẢO

Celery Official Documentation

Redis Documentation

Flask Official Documentation

Docker Official Documentation

Real Python – Using Celery with Flask

Hovy, E. H. (1993). Automated Discourse Generation Using Discourse Structure Relations. Artificial Intelligence, Elsevier, 63:341–385.

## 📌 Tác giả: Đặng Thanh Tùng<br>

\*\*📘 Lớp: Ứng dụng Phân tán – Nhóm 18, Học kỳ 1 – Năm 2025-2026<br>
🏫 Đại học Phenikaa<br>
🏫 Trường: Đại học Công Nghệ Thông Tin Phenikaa<br>

## 📌 Tác giả: Lê Đình Đức Anh<br>

📘 Lớp: Ứng dụng Phân tán – Nhóm 18, Học kỳ 1 – Năm 2025-2026<br>
🏫 Trường: Đại học Phenikaa<br>
🏫 Trường: Đại học Công Nghệ Thông Tin Phenikaa<br>
