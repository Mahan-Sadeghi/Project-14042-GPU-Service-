from datetime import datetime, timedelta
from jose import jwt
from passlib.context import CryptContext

# تنظیمات ساده (برای پروژه دانشگاهی همین‌طور ساده عالیه)
SECRET_KEY = "my_secret_key" # یک رمز دلخواه
ALGORITHM = "HS256"

# ابزار رمزنگاری پسورد
pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

# 1. تابع چک کردن پسورد (آیا پسورد وارد شده با دیتابیس یکی هست؟)
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# 2. تابع رمزنگاری پسورد (برای موقع ثبت‌نام)
def get_password_hash(password):
    return pwd_context.hash(password)

# 3. تابع ساخت توکن (کارت ورود)
def create_access_token(data: dict):
    to_encode = data.copy()
    # توکن بعد از 30 دقیقه منقضی میشه
    expire = datetime.utcnow() + timedelta(minutes=30)
    to_encode.update({"exp": expire})
    
    # ساخت کد نهایی
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
        
        
