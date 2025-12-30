from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

# فایل‌های خودمان (چون run.py مسیر رو درست کرده، دیگه sys.path نمی‌خواد)
from models import Base, engine, User, SessionLocal
from schemas import UserCreate, UserResponse, Token
from auth import get_password_hash, verify_password, create_access_token

# ساخت جدول‌های دیتابیس (اگر نباشن)
Base.metadata.create_all(bind=engine)

# شروع برنامه
app = FastAPI(title="GPU Service Platform")

# آدرس لاگین برای قفل Swagger
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# --- تابع کمکی: گرفتن دیتابیس ---
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ===========================
#  مسیرها (Routes)
# ===========================

@app.get("/")
def read_root():
    return {"message": "Welcome! System is ready."}

# 1. ثبت نام (Register)
@app.post("/users/register", response_model=UserResponse, tags=["Users"])
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    # بررسی تکراری نبودن
    if db.query(User).filter(User.username == user.username).first():
        raise HTTPException(status_code=400, detail="Username already exists")
    
    # ساخت و ذخیره کاربر
    new_user = User(
        username=user.username,
        hashed_password=get_password_hash(user.password), 
        role="user"
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

# 2. ورود (Login)
@app.post("/token", response_model=Token, tags=["Auth"])
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # پیدا کردن کاربر
    user = db.query(User).filter(User.username == form_data.username).first()
    
    # چک کردن رمز (دقت کن اینجا شد hashed_password)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    
    # صدور کارت ورود (Token)
    token = create_access_token(data={"sub": user.username})
    return {"access_token": token, "token_type": "bearer"}