from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.comment import Comment
from app.models.post import Post

# 게시글의 comment 리스트 반환 함수
def get_comment_by_post_id(db: Session, post_id: int) -> list[Comment]:
    # 게시글이 있는지 먼저 검증(게시글 있어야 댓글도 가능)
    post = db.get(Post, post_id)
    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="게시글을 찾을 수 없습니다."
        )

    # 정렬은 최신순으로
    return (
        db.query(Comment)
        .filter(Comment.post_id == post.id)
        .order_by(Comment.comment_id.asc())
        .all()
    )

def create_comment(db: Session, post_id: int, user_id: int, content: str) -> Comment:
    """로그인 사용자 comment 작성"""
    # 1. 게시글이 존재하지 않으면 404 error
    post = db.get(Post, post_id)
    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="게시글을 찾을 수 없습니다."
        )

    comment = Comment(
        content=content,
        post_id=post_id,
        user_id=user_id
    )
    db.add(comment)
    db.commit()
    db.refresh(comment)
    return comment

def delete_comment(db: Session, comment_id: int, user_id) -> None:
    """작성자 만 삭제가능"""
    comment = db.get(Comment, comment_id)
    if comment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="댓글이 없습니다.."
        )

    # 작성자 확인
    if comment.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="자신의 댓글만 삭제할 수 있습니다.")

    db.delete(comment)
    db.commit()
    db.refresh(comment)
    db.close()


