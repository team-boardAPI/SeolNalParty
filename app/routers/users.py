from fastapi import APIRouter, Depends, HTTPException

from app.core.database import SessionLocal
from app.core.security import hash_password
from app.dependencies.auth import get_current_user
from app.models.user import User
from app.schemas.user import UpdateUser, UserDelete, UserInfo

users_router = APIRouter(prefix="/users", tags=["users"])


def compare_id(user_id, current_user):
    if current_user.user_id != user_id:
        raise HTTPException(status_code=403, detail="Forbidden")


@users_router.get("/{user_id}", response_model=UserInfo)
def user_info(user_id: int, current_user=Depends(get_current_user)):
    compare_id(user_id, current_user)
    return current_user


@users_router.put("/{user_id}", response_model=UserInfo)
def update_user(user_id: int, data: UpdateUser, current_user=Depends(get_current_user)):
    compare_id(user_id, current_user)

    with SessionLocal() as db:
        db_user = db.query(User).filter(User.user_id == user_id).first()
        if db_user is None:
            raise HTTPException(status_code=404, detail="User not found")
        db_data = data.model_dump(exclude_unset=True)
        db_data["password"] = hash_password(pw=db_data["password"])
        db.query(User).filter(User.user_id == user_id).update(db_data)
        db.commit()
        db.refresh(db_user)
    return db_user


@users_router.delete("/{user_id}", response_model=UserDelete)
def delete_user(user_id: int, current_user=Depends(get_current_user)):
    compare_id(user_id, current_user)
    with SessionLocal() as db:
        deleted_user = db.query(User).filter(User.user_id == user_id).delete()
        if not deleted_user:
            raise HTTPException(status_code=404, detail="User not found")
        db.commit()

    return {"message": "User deleted"}
