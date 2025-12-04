
from sqlalchemy import Column, Integer, String, Text, DateTime, func
from app.db.database import Base

from sqlalchemy.orm import Mapped, mapped_column


class User(Base): 
    __tablename__= "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    phone: Mapped[str]= mapped_column(String(20), unique=True)
    email: Mapped[str] = mapped_column(String(255), unique=True)
    
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    
    address: Mapped[str] = mapped_column(String(255))
    name: Mapped[str] = mapped_column(String(100))
    
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), default=func.now())
    updated_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), default=func.now(), onupdate=func.now())

