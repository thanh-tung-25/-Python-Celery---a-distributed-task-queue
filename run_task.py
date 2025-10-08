from celery_app.tasks import add, reverse_text

def main():
    r = add.delay(10, 20)
    print("📤 Sent add task id:", r.id)
    print("📥 Result:", r.get(timeout=30))

    r2 = reverse_text.delay("Celery Distributed Task Queue")
    print("📤 Sent reverse_text id:", r2.id)
    print("📥 Result:", r2.get(timeout=30))

if __name__ == "__main__":
    main()
