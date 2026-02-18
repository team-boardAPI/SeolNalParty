# 로그인 유저 정보는 토큰에서
# 삭제는 작성자만 가능

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session


from app.dependencies.auth import get_current_user # import 경로 수정
from app.core.database import get_db
from app.schemas.comment import CommentCreate, CommentRead
from app.services import comment_service
from app.models.user import User # current_user 타입 힌트용(경로 수정)
from app.core.database import SessionLocal

router = APIRouter(prefix="/posts", tags=["comments"])


@router.get("/{post_id}/comments")
def list_comments(post_id: int, db: Session = Depends(get_db)):
    comments = comment_service.get_comment_by_post_id(db=db, post_id=post_id)
    data = [CommentRead.model_validate(c).model_dump() for c in comments]
    return {
    "success": True,
    "data": data,
    "message": "success"
}


@router.post("/{post_id}/comments", status_code=status.HTTP_201_CREATED)
def create_comment(
        post_id: int,
        payload: CommentCreate,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user),
):
        # 로그인 사용자 comment 작성
        comment = comment_service.create_comment(
            db=db,
            post_id=post_id,
            user_id=current_user.user_id,
            content=payload.content
        )

        return {
            "success": True,
            "data": CommentRead.model_validate(comment).model_dump(),
            "message": "success"
        }


@router.delete("/{post_id}/comments/{comment_id}")
def delete_comment(
        post_id: int,
        comment_id: int,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user),
):
    # 작성자만 삭제
    comment_service.delete_comment(
        db=db,
        comment_id=comment_id,
        user_id=current_user.user_id
    )

    return {
        "success": True,
        "message": "success"}


