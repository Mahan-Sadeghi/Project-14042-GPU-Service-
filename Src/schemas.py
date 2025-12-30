from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# =======================
# بخش ۱: مدل‌های مربوط به کاربر (User)
# =======================

class UserBase(BaseModel):
    username: str
    role: str = "user"  # نقش پیش‌فرض: کاربر عادی

# این مدل برای زمانیه که کاربر میخواد ثبت‌نام کنه (پسورد رو میده)
class UserCreate(UserBase):
    password: str

# این مدل برای زمانیه که میخوایم اطلاعات رو به کاربر نشون بدیم (پسورد رو حذف کردیم)
class UserResponse(UserBase):
    id: int
    created_at: datetime
    # اینجا خبری از password نیست!

    class Config:
        from_attributes = True

# مدل برای توکن ورود (Login)
class Token(BaseModel):
    access_token: str
    token_type: str

# =======================
# بخش ۲: مدل‌های مربوط به کارها (Jobs)
# =======================

class JobBase(BaseModel):
    gpu_type: str          # نوع گرافیک: مثلا T4 یا A100
    gpu_count: int         # تعداد گرافیک درخواستی
    estimated_hours: int   # پیش‌بینی زمان اجرا
    script_content: str    # محتوای اسکریپت پایتون
    data_path: str         # آدرس فایل داده‌ها
    is_sensitive: bool = False  # آیا داده محرمانه است؟ (طبق خواسته استاد)

# مدل برای ایجاد جاب جدید
class JobCreate(JobBase):
    pass

# مدل برای نمایش جاب به کاربر
class JobResponse(JobBase):
    id: int
    user_id: int
    status: str            # وضعیت: pending, running, completed
    submitted_at: datetime

    class Config:
        from_attributes = True

# --- این کلاس مخصوص توکن است ---
class Token(BaseModel):
    access_token: str
    token_type: str