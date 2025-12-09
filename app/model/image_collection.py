from sqlalchemy import Column, Integer, String, Text, DateTime, func, ForeignKey
from app.db.database import Base
from sqlalchemy.orm import relationship, mapped_column, Mapped
# from app.model.user_model import User
# from app.model.image_version import ImageVersion


# from typing
class ImageCollection(Base):
    __tablename__ = "image_collections"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    prompt: Mapped[str] = mapped_column(
        Text, nullable=False
    )  # TODO maybe limit of prompt length add
    model: Mapped[str] = mapped_column(String(100), nullable=False)
    style: Mapped[str] = mapped_column(String(100), nullable=True)

    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id"), nullable=False
    )

    user: Mapped["User"] = relationship("User", back_populates="image_collections")
    image_version: Mapped[list["ImageVersion"]] = relationship(
        "ImageVersion", back_populates="collection", cascade="all, delete-orphan"
    )

    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )
