from sqlalchemy import Column, Integer, String

from app.core.database import Base

# from sqlalchemy.orm import relationship



class User(Base):

    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True)
    login_id = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    user_name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    # posts = relationship("Post", back_populates="author")
