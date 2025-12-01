
from sqlalchemy import Column, Integer, String, Text, DateTime, func
from db.database import Base

class ImageCollection(Base):
    __tablename__ = "img_collections"
    id = Column(Integer, primary_key=True, index=True)
    prompt = Column(Text) # TODO maybe limit of prompt length add
    model = Column(String(100))
    image_url = Column(Text)
    
    user_id = Column(Integer)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    
    