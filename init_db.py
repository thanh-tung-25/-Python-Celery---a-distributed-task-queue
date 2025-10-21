# init_db.py
from database.database import app, db

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        print("✅ Database & bảng đã được khởi tạo thành công!")