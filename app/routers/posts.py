from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.dependencies.auth import get_current_user
from app.models.user import User
# 서비스
from app.schemas.post import (CommonResponse, CreatePost, PostResponseDetail,
                              PostResponseList, UpdatePost)
from app.services import post_service

router = APIRouter(
    prefix="/posts",
    tags=["posts"],
)


# app/routers/post.py


# 1. 게시글 전체 조회
@router.get("/", response_model=CommonResponse[List[PostResponseList]])
def get_posts(db: Session = Depends(get_db)):
    posts = post_service.get_all_posts(db=db)
    # message 생략 -> 기본값 "요청 성공" 사용됨
    return CommonResponse(data=posts)


# 2. 게시글 상세 조회
@router.get("/{post_id}", response_model=CommonResponse[PostResponseDetail])
def get_post(post_id: int, db: Session = Depends(get_db)):
    post = post_service.get_post(db=db, post_id=post_id)
    return CommonResponse(data=post)


# 3. 게시글 등록
@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=CommonResponse[PostResponseDetail],
)
def create_post(
    post: CreatePost,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    new_post = post_service.create_post(db=db, post=post, user_id=current_user.user_id)
    return CommonResponse(data=new_post)


# 4. 게시글 수정
@router.put("/{post_id}", response_model=CommonResponse[PostResponseDetail])
def update_post(
    post_id: int,
    post: UpdatePost,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    updated_post = post_service.update_post(
        db=db, post_id=post_id, post_update=post, user_id=current_user.user_id
    )
    return CommonResponse(data=updated_post)


# 5. 게시글 삭제 (데이터가 없으므로 생략 가능)
@router.delete("/{post_id}", response_model=CommonResponse[None])
def delete_post(
    post_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    post_service.delete_post(db=db, post_id=post_id, user_id=current_user.user_id)
    return CommonResponse()  # success=True, data=None, message="요청 성공"


# 6. 좋아요 추가
@router.post("/{post_id}/like", response_model=CommonResponse[None])
def like_post(
    post_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    post_service.like_post(db=db, post_id=post_id, user_id=current_user.user_id)
    return CommonResponse()
