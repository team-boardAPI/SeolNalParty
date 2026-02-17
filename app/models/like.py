from sqlalchemy import Column, ForeignKey, Integer, UniqueConstraint
from sqlalchemy.orm import relationship

# Base: declarative_base (테이블 맵핑 기반 클래스)
from app.core.database import Base

class Like(Base):
    # 테이블 정의
    __tablename__ = "like"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
    post_id = Column(Integer, ForeignKey("post.id", ondelete="CASCADE"), nullable=False)

    # 제약 조건
    __table_args__ = (UniqueConstraint("user_id", "post_id"),)

    # 데이터간의 관꼐
    user = relationship("User", back_populates="likes")
    post = relationship("Post", back_populates="likes")
