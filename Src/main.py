from fastapi import FastAPI
from models import Base, engine

# ۱. ساخت اپلیکیشن اصلی
# اینجا مشخصات پروژه رو میدیم که توی داکیومنت‌ها نشون داده بشه
app = FastAPI(
    title="GPU Service Platform",
    description="سیستم مدیریت منابع پردازشی - پروژه درس برنامه‌نویسی پیشرفته",
    version="1.0.0"
)

# ۲. ساخت خودکار دیتابیس
# این دستور به SQLAlchemy میگه: "برو تمام مدل‌هایی که ساختیم رو تبدیل کن به جدول دیتابیس"
# اگر فایل gpu_service.db وجود نداشته باشه، همینجا ساخته میشه.
Base.metadata.create_all(bind=engine)

# ۳. یک مسیر ساده برای تست (Home Page)
@app.get("/")
def read_root():
    return {"message": "Welcome to GPU Service Platform! System is Ready. 🚀"}



