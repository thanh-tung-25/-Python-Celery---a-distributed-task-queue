# 📧 HỆ THỐNG GỬI EMAIL PHÂN TÁN SỬ DỤNG FLASK VÀ CELERY<br>
## 🧩 1. Giới thiệu

Đề tài “Xây dựng hệ thống gửi email phân tán sử dụng Flask và Celery” được thực hiện nhằm giải quyết bài toán xử lý bất đồng bộ khi gửi email hàng loạt.

Thay vì để máy chủ Flask trực tiếp gửi từng email (dễ gây chậm hoặc treo khi có nhiều yêu cầu), hệ thống sử dụng Celery để tách quá trình gửi email thành các tác vụ độc lập (task) và xử lý song song bằng các tiến trình worker.

Redis được dùng làm hàng đợi trung gian để lưu trữ và điều phối các tác vụ này.
Hệ thống giúp tăng hiệu suất, giảm tải cho máy chủ, và đảm bảo khả năng mở rộng trong môi trường triển khai thực tế.

## ⚙️ 2. Kiến trúc hệ thống

Hệ thống gồm ba thành phần chính:

### 2.1. Flask API

Nhận yêu cầu gửi email từ người dùng thông qua giao diện web.

Gửi task đến Celery qua Redis.

Cung cấp API kiểm tra trạng thái tác vụ.

### 2.2. Celery Worker

Nhận các task từ Redis.

Thực hiện gửi email thật qua SMTP.

Gửi kết quả xử lý trả lại cho Flask.

### 2.3. Redis

Đóng vai trò hàng đợi trung gian, giúp Flask và Celery giao tiếp với nhau.

### 2.4. Sơ đồ hoạt động hệ thống
Người dùng → Flask API → Redis Queue → Celery Worker → SMTP Server → Email người nhận

## 🧠 3. Công nghệ sử dụng
Công nghệ Vai trò
Python 3.x Ngôn ngữ lập trình chính
Flask Xây dựng REST API
Celery Xử lý tác vụ nền, bất đồng bộ
Redis Hàng đợi lưu trữ task
SMTP (Gmail) Gửi email thật
HTML/CSS/JS Xây dựng giao diện người dùng
Docker Compose (tùy chọn) Triển khai hệ thống đồng bộ
## 📂 4. Cấu trúc thư mục dự án
.
├── celery_app/ <br>
│ ├── **init**.py <br>
│ ├── celery_config.py <br>
│ ├── tasks.py <br>
│ └── email_utils.py <br>
├── api_server.py <br>
├── worker.py <br>
├── run_task.py <br>
├── .env <br>
├── docker-compose.yml <br>
├── requirements.txt <br>
└── frontend/ <br>
├── index.html <br>
├── script.js <br>
└── style.css

## ⚙️ 5. Cấu hình môi trường (.env)
FLASK_ENV=development<br>
PORT=5000

# Redis

CELERY_BROKER_URL=redis://localhost:6379/0 <br>
CELERY_RESULT_BACKEND=redis://localhost:6379/1 

# SMTP

MAIL_SERVER=smtp.gmail.com <br>
MAIL_PORT=587  <br>
MAIL_USERNAME=your_email@gmail.com  <br>
MAIL_PASSWORD=your_app_password  <br>
MAIL_USE_TLS=True  <br>
MAIL_DEFAULT_SENDER=your_email@gmail.com

## 🚀 6. Cách cài đặt và chạy dự án
Cách 1: Chạy trực tiếp (Windows + virtualenv)

### 1. Tạo môi trường ảo và cài đặt thư viện

python -m venv venv  <br>
.\venv\Scripts\Activate.ps1  <br>
pip install -r requirements.txt

### 2. Khởi động Redis (cần cài sẵn Redis)

redis-server

### hoặc dùng Docker:

docker run -d -p 6379:6379 redis

### 3. Mở terminal 1: chạy Flask API

python api_server.py

### 4. Mở terminal 2: chạy Celery worker

celery -A celery_app.celery_config.app worker --loglevel=info -P solo

### 5. Gửi email thử nghiệm

Truy cập http://localhost:5000 → nhập nội dung email → nhấn "Gửi"  <br>

Cách 2: Chạy qua Docker Compose

### Chạy toàn bộ hệ thống

docker compose up --build  <br>

Docker sẽ tự động khởi chạy Flask (API Web), Celery Worker, và Redis.

### ✅ 7. Kết luận

Đề tài đã xây dựng thành công hệ thống gửi email phân tán sử dụng Flask, Celery và Redis.  <br>
Hệ thống hoạt động ổn định, có khả năng:  <br>

Gửi email thật qua SMTP.  <br>

Xử lý song song nhiều tác vụ.  <br>

Dễ dàng mở rộng và triển khai thực tế.  <br>

Việc áp dụng mô hình xử lý bất đồng bộ đã giúp tăng hiệu năng và đảm bảo khả năng chịu tải cao khi có nhiều yêu cầu đồng thời.

### 🚀 8. Hướng phát triển

Xây dựng trang quản trị theo dõi trạng thái các task gửi email.  <br>

Thêm chức năng hẹn giờ gửi email hoặc gửi hàng loạt theo danh sách tệp CSV.  <br>

Lưu log và thống kê số lượng email gửi thành công/thất bại. <br>

Nâng cấp hệ thống sử dụng RabbitMQ hoặc AWS SQS để tối ưu hiệu suất.

Triển khai hệ thống lên nền tảng Cloud như Heroku, AWS, hoặc DockerHub.
