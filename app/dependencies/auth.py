from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.services.auth_service import get_authorized_user

bearer_scheme = HTTPBearer()


# 권한 확인
def get_current_user(
    auth: HTTPAuthorizationCredentials = Depends(bearer_scheme),
):
    current_user = get_authorized_user(auth.credentials)
    return current_user
