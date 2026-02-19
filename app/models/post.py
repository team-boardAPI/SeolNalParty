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
    comments = relationship(
        "Comment", back_populates="post", cascade="all, delete-orphan"
    )
    likes = relationship("Like", back_populates="post", cascade="all, delete-orphan")

    # Pydantic이 요구하는 'like_count'를 계산해서 제공
    @property
    def like_count(self) -> int:
        return len(self.likes) if self.likes else 0

    # Pydantic이 요구하는 'post_comments'를 제공
    # (모델의 관계명이 'comments'이므로 이를 'post_comments'라는 이름으로도 접근 가능하게 함)
    @property
    def post_comments(self):
        return self.comments
