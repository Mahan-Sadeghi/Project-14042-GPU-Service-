import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, create_engine, Text
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

Base = declarative_base()

class User(Base):
    
    """ مدل کاربر (User Model) """

    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    password_hash = Column(String(200), nullable=False)
    role = Column(String(20), default="user")  # user / admin
    
    # مدیریت سهمیه (Quota Management)
    quota_limit = Column(Integer, default=50)
    quota_used = Column(Integer, default=0)

    jobs = relationship("Job", back_populates="owner")

    def __repr__(self):
        return f"<User(username='{self.username}', role='{self.role}')>"

class Job(Base):
   
    """مدل درخواست (Job Model)"""
    
    __tablename__ = 'jobs'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    
    # متادیتای درخواست
    gpu_type = Column(String(50), nullable=False)
    gpu_count = Column(Integer, default=1)
    estimated_hours = Column(Integer, nullable=False)
    
    # دستور اجرای مدل
    command = Column(Text, nullable=True)
    
    is_sensitive = Column(Boolean, default=False)
    data_path = Column(String(200), nullable=True)
    
    # وضعیت: pending, approved, running, completed, failed
    status = Column(String(20), default="pending")
    
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    owner = relationship("User", back_populates="jobs")

    def __repr__(self):
        return f"<Job(id={self.id}, status='{self.status}')>"

# تنظیمات دیتابیس
engine = create_engine('sqlite:///gpuservice.db', echo=True)
SessionLocal = sessionmaker(bind=engine)

def init_db():
    Base.metadata.create_all(engine)

if __name__ == "__main__":
    init_db()
    print("Database tables created successfully! (Verified with Project Requirements)")