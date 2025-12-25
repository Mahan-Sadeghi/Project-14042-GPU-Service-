import jwt
import datetime
from passlib.context import CryptContext

# --- تنظیمات امنیتی ---
# در پروژه واقعی این کلید باید مخفی باشد
SECRET_KEY = "my_super_secret_key_for_project_14042"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30  # اعتبار توکن: ۳۰ دقیقه

# تنظیمات هش کردن پسورد (سعی می‌کند از bcrypt استفاده کند)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    """
    بررسی میکند آیا پسورد وارد شده با پسورد هش شده در دیتابیس یکی است؟
    """
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    """
    تبدیل پسورد معمولی به هش (رمزنگاری شده)
    """
    return pwd_context.hash(password)

def create_access_token(data: dict):
    """
    ساخت توکن JWT برای کاربر لاگین شده.
    """
    to_encode = data.copy()
    expire = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# بخش تست خودکار (لحظه حقیقت) 

if __name__ == "__main__":
    print("Testing Security Libraries")
    
    # تست ۱: آیا پسورد هش میشود؟
    try:
        my_pass = "student123"
        hashed = get_password_hash(my_pass)
        print(f"✅ Hashing Check: PASSED")
        print(f"   Original: {my_pass}")
        print(f"   Hashed:   {hashed}")
    except Exception as e:
        print(f"❌ Hashing FAILED: {e}")

    # تست ۲: آیا توکن ساخته میشود؟
    try:
        token = create_access_token({"sub": "ali_user", "role": "admin"})
        print(f"✅ Token Check: PASSED")
        print(f"   Generated Token: {token}")
    except Exception as e:
        print(f"❌ Token FAILED: {e}")
        
        