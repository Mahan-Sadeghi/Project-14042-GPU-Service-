import uvicorn
import os
import sys

if __name__ == "__main__":
    # ۱. اول میریم داخل پوشه src (انگار دستور cd src رو زدیم)
    os.chdir("src")
    
    # ۲. مسیر فعلی رو به پایتون می‌شناسونیم تا فایل‌ها رو پیدا کنه
    sys.path.append(".")

    # ۳. حالا سرور رو روشن می‌کنیم (دیگه src.main نمیگیم، چون رفتیم توش)
    print("🚀 Starting GPU Service Platform...")
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)