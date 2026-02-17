from typing import List

from fastapi import HTTPException, status
from sqlalchemy.orm import joinedload

from app.core.database import SessionLocal
# from app.models.comment import Comment
from app.models.like import Like
from app.models.post import Post
from app.schemas.post import CreatePost, UpdatePost


#  게시물 등록
def create_post(post: CreatePost, user_id: int) -> Post:
    # model_dump : 객체를 딕셔너리 형태로 변환
    db = SessionLocal()
    new_post = Post(**post.model_dump(), user_id=user_id)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    db.close()
    return new_post


# 게시물 전체 조회
def get_all_posts() -> List[Post]:
    db = SessionLocal()
    posts = db.query(Post).all()
    db.close()
    return posts


# 게시물 상세 조회
def get_post(post_id: int):
    db = SessionLocal()
    # 좋아요 정보를 가져오기 위해 조인
    post = (
        db.query(Post)
        .options(joinedload(Post.likes))
        .filter(Post.id == post_id)
        .first()
    )
    # 예외처리
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{post_id} 인 게시글이 존재 하지 않습니다",
        )
    # post_id like테이블의 행수
    post.likes_count = len(post.likes)
    db.close()
    return post


# 게시물 수정
def update_post(post_id: int, post_update: UpdatePost) -> Post:
    db = SessionLocal()
    post_query = db.query(Post).filter(Post.id == post_id)
    post = post_query.first()
    # 예외처리
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{post_id}인 게시글이 존재하지 않습니다",
        )
    # exclude_unset=True : 변경된 데이터만 추출
    # synchronize_session=False : db에 데이터를 우선 수정 파이썬 메모리에 있는 데이터는 뒤로 미룸
    update_data = post_update.model_dump(exclude_unset=True)

    post_query.update(update_data, synchronize_session=False)
    db.commit()
    db.refresh(post)
    db.close()
    return post


# 게시물 삭제
def delete_post(post_id: int) -> dict:
    db = SessionLocal()
    post_query = db.query(Post).filter(Post.id == post_id)
    post = post_query.first()
    # 예외처리
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{post_id}인 게시글이 존재하지 않습니다",
        )
    post_query.delete(synchronize_session=False)
    db.commit()
    db.close()
    return {"message": f"{post_id}인 게시물이 삭제되었습니다"}


# 좋아요 추가 기능
def like_post(post_id: int, user_id: int) -> dict:
    db = SessionLocal()
    post = db.query(Post).filter(Post.id == post_id).first()

    # 예외처리
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{post_id}인 게시글이 존재하지 않습니다",
        )

    # 좋아요 조회
    exist_like = (
        db.query(Like)
        .filter(Like.post_id == post_id)
        .filter(Like.user_id == user_id)
        .first()
    )

    # 종아요가 있을 경우
    if exist_like:
        db.delete(exist_like)
        db.commit()
        db.close()
        return {"message": "좋아요가 삭제 되었습니다"}
    # 좋아요가 없을 경우
    else:
        new_like = Like(post_id=post_id, user_id=user_id)
        db.add(new_like)
        db.commit()
        db.close()
        return {"message": "좋아요가 추가 되었습니다"}
