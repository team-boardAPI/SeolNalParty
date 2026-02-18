from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, Text
from sqlalchemy.orm import relationship

from app.core.database import Base


class Comment(Base):
    __tablename__ = "comments"
    comment_id = Column(Integer, primary_key=True, index=True)
    content = Column(Text, nullable=False)
    post_id = Column(
        Integer, ForeignKey("posts.posts.id", ondelete="CASCADE"), nullable=False
    )
    user_id = Column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    date_posted = Column(DateTime, nullable=False, default=datetime.utcnow)

    post = relationship("Post", back_populates="comments")
    user = relationship("User", back_populates="comments")
