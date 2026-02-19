from fastapi import APIRouter

from app.schemas.token import (CreateUser, LoginSchema, LogoutSchema,
                               RefreshToken)
from app.services.auth_service import (login_user, logout_user,
                                       refresh_access_token, register_user)

auth_router = APIRouter(prefix="/auth", tags=["auth"])


# 회원가입
@auth_router.post("/register")
def create_user(user: CreateUser):
    data = register_user(user)
    return data


# 로그인
@auth_router.post("/login")
def login(user: LoginSchema):
    user_info = login_user(user)
    return user_info


# 로그아웃
@auth_router.post("/logout")
def logout(tokens: LogoutSchema):
    access_token = tokens.access_token
    refresh_token = tokens.refresh_token
    return logout_user(access_token=access_token, refresh_token=refresh_token)


# 액세스 토큰 재발급
@auth_router.post("/refresh")
def refresh(refresh_token: RefreshToken):
    access_token = refresh_access_token(refresh_token.refresh_token)
    return access_token
