from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


# comment 공통
class CommentBase(BaseModel):
    content: str = Field(..., min_length=1, max_length=1000)


# 코멘트 생성
class CommentCreate(CommentBase):
    # post_id는 path로 받고 user_id는 토큰으로 받음
    pass


# 게시글 상세 조회 시 댓글 목록
class CommentRead(CommentBase):
    comment_id: int
    post_id: int
    user_id: int
    date_posted: datetime

    # ORM 객체를 pydantic으로 변환 가능
    model_config = ConfigDict(from_attributes=True)


class CommentDelete(BaseModel):
    comment_id: int
    message: str = "댓글이 삭제되었습니다."
