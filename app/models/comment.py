from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey


class Comment(Base):
    __tablename__ = "comments"

    id: Mapped[int] = mapped_column(primary_key=True)
    content: Mapped[str] = mapped_column(nullable=False)
    post_id: Mapped[int] = mapped_column(ForeignKey("posts.id"))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))


    def __repr__(self):
        return f"Comment(id={self.id}, content={self.content}, post_id={self.post_id}, user_id={self.user_id})"


