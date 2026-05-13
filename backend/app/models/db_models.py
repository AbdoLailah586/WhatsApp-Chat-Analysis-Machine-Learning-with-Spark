from sqlalchemy import Column, Integer, String, Boolean, DateTime, Float, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime

class Upload(Base):
    __tablename__ = "uploads"
    
    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, index=True)
    uploaded_at = Column(DateTime, default=datetime.utcnow)
    status = Column(String, default="pending")
    message_count = Column(Integer, default=0)
    
    messages = relationship("Message", back_populates="upload", cascade="all, delete-orphan")

class Message(Base):
    __tablename__ = "messages"
    
    id = Column(Integer, primary_key=True, index=True)
    upload_id = Column(Integer, ForeignKey("uploads.id"), index=True)
    sender = Column(String, index=True)
    timestamp = Column(DateTime, index=True)
    content = Column(Text)
    category = Column(String, index=True, nullable=True)
    confidence_score = Column(Float, nullable=True)
    is_media = Column(Boolean, default=False)
    
    upload = relationship("Upload", back_populates="messages")
