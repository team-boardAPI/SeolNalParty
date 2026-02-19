# pydantic 파이썬에서 데이터를 객체화하는 모듈
from datetime import datetime
#  데이터의 타입 힌트 , 수정시에 수정하는 데이터와 수정하지 않는 데이터의 구분
from typing import Generic, List, Optional, TypeVar

from pydantic import BaseModel, ConfigDict, Field

from .comment import CommentRead  # 코멘트 응답 스키마 불러오기
from .user import UserInfo


# 공통 스키마
class PostBase(BaseModel):
    #  ... (Ellipsis) : 기본값 없이 검증 조건을 사용학고 클라이언트로 부터 값을 무조건 받아야 할때
    title: str = Field(
        ...,
        min_length=1,
        max_length=100,
        title="게시글 제목",
        examples=["입력한 게시글 제목"],
        description="1자 이상 100자 이하 입력 필수",
    )


# 생성 및 수정 스키마: 클라이언트 보낼 데이터
# 생성  스키마
class CreatePost(PostBase):
    content: str = Field(
        min_length=1,
        title="게시글 내용",
        examples=["입력한 게시글 내용"],
        description="1자 이상 입력",
    )


# 수정 스키마
class UpdatePost(BaseModel):
    # default는 None
    title: Optional[str] = Field(None, min_length=1, max_length=100)
    content: Optional[str] = Field(None, min_length=1)


# 응답 스키마
# db에서 클라이언트로 보낼 데이터
class PostResponseList(PostBase):
    id: int
    user_id: int
    date_posted: datetime
    author: UserInfo
    # 좋아요 (계산으로 값 생성)
    # pydantic 설정 : 객첵 형태로도 데이터를 읽을 수 있게 설정
    model_config = ConfigDict(from_attributes=True)


# 상세 조회 스키마 (좋아요 포함)
class PostResponseDetail(PostResponseList):
    content: str
    like_count: int
    post_comments: List[CommentRead]


# 요청 응답 스키마
T = TypeVar("T")


class CommonResponse(BaseModel, Generic[T]):
    success: bool = True
    data: Optional[T] = None
    message: str = "요청 성공"
