from typing import List

from fastapi import APIRouter

# 서비스
from app.schemas.post import (CreatePost, PostResponseDetail, PostResponseList,
                              UpdatePost)
from app.services import post_service

router = APIRouter(
    prefix="/posts",
    tags=["posts"],
)


# 게시글 조회
@router.get("/", response_model=List[PostResponseList])
def get_posts():
    return post_service.get_all_posts()


# 게시글 상세 조회
@router.post("/", response_model=PostResponseDetail)
def get_post(post_id: int) -> PostResponseDetail:
    return post_service.get_post(post_id=post_id)


# 게시글 등록
@router.post("/", response_model=CreatePost)
def create_post(post: CreatePost):
    return post_service.create_post(post)


# 게시글 수정
@router.put("/{post_id}", response_model=UpdatePost)
def update_post(post_id: int, post: UpdatePost):
    return post_service.update_post(post_id=post_id, post_update=post)


# 게시글 삭제
@router.delete("/{post_id}")
def delete_post(post_id: int):
    return post_service.delete_post(post_id=post_id)


# 좋아요 추가
@router.get("/{post_id}/like")
def like_post(post_id: int):
    return post_service.like_post(post_id=post_id)
