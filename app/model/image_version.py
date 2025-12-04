
from sqlalchemy import Column, Integer, String, Text, DateTime,Boolean, func, ForeignKey
from app.db.database import Base
from sqlalchemy.orm import relationship, mapped_column, Mapped
from app.model.image_collection import ImageCollection

class ImageVersion(Base):
    __tablename__ = "image_versions"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    isFinal : Mapped[bool] = mapped_column(Boolean)
    # title: Mapped[str] = mapped_column(String(255), nullable=True) 
    
    image_url:Mapped[str] = mapped_column(Text, nullable=False)
    
    parent_id: Mapped[int] = mapped_column(Integer, ForeignKey("image_versions.id"), nullable=True)
    parent: Mapped["ImageVersion"] = relationship("ImageVersion", remote_side=[id])
    
    collection_id : Mapped[int] = mapped_column(Integer, ForeignKey("image_collections.id"), nullable=False)
    collection: Mapped["ImageCollection"] = relationship("ImageCollection", back_populates="image_version")
    
    
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    
    
    
    