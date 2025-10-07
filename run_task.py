from celery_app.tasks import add

def main():
    result = add.delay(10, 20)
    print("📤 Đã gửi task cộng 10 + 20")
    print("📥 Kết quả:", result.get(timeout=10))

if __name__ == "__main__":
    main()
