from celery_app.tasks import add, reverse_text

if __name__ == "__main__":
    # Gửi task cộng 10 + 20
    result = add.delay(10, 20)
    print("Đã gửi task cộng 10 + 20")
    print("Kết quả:", result.get(timeout=10))

    # Gửi task đảo chuỗi
    res2 = reverse_text.delay("Celery Distributed Task Queue")
    print("Đã gửi task đảo chuỗi")
    print("Kết quả:", res2.get(timeout=10))
