from fastapi import HTTPException

import app.core.security as sc
from app.core.database import SessionLocal
from app.core.security import (
    BLOCKLIST,
    create_access_token,
    create_refresh_token,
    verify_access_token,
    verify_refresh_token,
)
from app.models.user import User


# 기존 로그인 아이디와 일치하는지 확인
def check_by_login_id(user, db):
    login_id = db.query(User).filter(User.login_id == user.login_id).first()
    if login_id:
        raise HTTPException(status_code=400, detail="Login_id is already exist")


# 기존 이메일과 일치하는지 확인
def check_by_email(user, db):
    email = db.query(User).filter(User.email == user.email).first()
    if email:
        raise HTTPException(status_code=400, detail="Email is already exist")


# 회원정보 디비에 저장
def register_user(user):
    with SessionLocal() as db:
        check_by_login_id(user=user, db=db)
        check_by_email(user=user, db=db)

        hashed_pw = sc.hash_password(pw=user.password)
        dict_data = user.model_dump()
        dict_data["password"] = hashed_pw
        new_user = User(**dict_data)

        db.add(new_user)
        db.commit()
        db.refresh(new_user)

    return new_user


# 로그인 아이디 확인
def get_by_login_id(user, db):
    db_user = db.query(User).filter(User.login_id == user.login_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="Login_id not found")
    return db_user


# 로그인 실행 로직
def login_user(user):
    with SessionLocal() as db:
        db_user = get_by_login_id(user, db)
        verified = sc.verify_password(
            plain_pw=user.password, hashed_pw=db_user.password
        )
        if not verified:
            raise HTTPException(status_code=401, detail="Incorrect password")
        else:
            data = {"sub": str(db_user.user_id)}
            access_token = str(create_access_token(data))
            refresh_token = str(create_refresh_token(data))

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
        }


# 권한 확인
def get_authorized_user(access_token):
    payload = verify_access_token(access_token)
    if payload["jti"] in BLOCKLIST:
        raise HTTPException(status_code=403, detail="Unauthorized")
    user_id = payload["sub"]
    with SessionLocal() as db:
        db_user = db.query(User).filter(User.user_id == int(user_id)).first()
        if db_user is None:
            raise HTTPException(status_code=404, detail="User not found")
        return db_user


# 액세스 토큰 재발급
def refresh_access_token(refresh_token: str):
    payload = verify_refresh_token(refresh_token)
    access_token = str(create_access_token({"sub": str(payload["sub"])}))
    return {
        "access_token": access_token,
        "token_type": "bearer",
    }


# 로그아웃 실행 로직
def logout_user(access_token: str, refresh_token: str):
    access_payload = verify_access_token(access_token)
    refresh_payload = verify_refresh_token(refresh_token)
    BLOCKLIST.add(access_payload["jti"])
    BLOCKLIST.add(refresh_payload["jti"])

    return {"message": "You have been logged out"}
