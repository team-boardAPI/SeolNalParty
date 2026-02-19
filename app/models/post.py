from sqlalchemy import (Column, DateTime, ForeignKey, Integer, String, Text,
                        func)
from sqlalchemy.orm import relationship

# Base: declarative_base (테이블 맵핑 기반 클래스)
from app.core.database import Base


class Post(Base):
    # 테이블 정의
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    date_posted = Column(
        # timezone : 표준시간,  sever_default : db를 기준. func.now() : db에 데이터 입력 시점
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)

    # 데이터 관계
    author = relationship("User", back_populates="posts")
    comments = relationship("Comment", back_populates="posts")
    likes = relationship("Like", back_populates="posts")
