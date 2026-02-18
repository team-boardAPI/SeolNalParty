import os
import uuid
from datetime import datetime, timedelta

import bcrypt
from dotenv import load_dotenv
from fastapi import HTTPException
from jose import ExpiredSignatureError, JWTError, jwt

# 로그아웃 용 블럭리스트
BLOCKLIST = set()


# 암호화 및 토큰 발급에 필요한 상수
load_dotenv()
ACCESS_SECRET_KEY = os.getenv("ACCESS_SECRET_KEY")
REFRESH_SECRET_KEY = os.getenv("REFRESH_SECRET_KEY")
ALGORITHM = "HS256"
ALGORITHMS = ["HS256"]
ACCESS_TOKEN_EXPIRE_MINUTES = 60
REFRESH_TOKEN_EXPIRE_DAYS = 3


# 패스워드 암호화
def hash_password(pw: str) -> str:
    pw_bytes = pw.encode("utf-8")
    hashed = bcrypt.hashpw(pw_bytes, bcrypt.gensalt())
    return hashed.decode("utf-8")


# 사용자 입력 패스워드와 젖아된 패스워드가 같은지 확인
def verify_password(plain_pw: str, hashed_pw: str) -> bool:
    return bcrypt.checkpw(plain_pw.encode("utf-8"), hashed_pw.encode("utf-8"))


# 액세스 토큰 발급
def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire, "jti": str(uuid.uuid4())})

    access_token = jwt.encode(
        claims=to_encode, key=ACCESS_SECRET_KEY, algorithm=ALGORITHM
    )

    return access_token


# 리프레시 토큰 발급
def create_refresh_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)

    to_encode.update({"exp": expire, "jti": str(uuid.uuid4())})

    refresh_token = jwt.encode(
        claims=to_encode, key=REFRESH_SECRET_KEY, algorithm=ALGORITHM
    )

    return refresh_token


# 액세스 토큰 유효성 확인
def verify_access_token(access_token: str):

    try:
        payload = jwt.decode(
            token=access_token, key=ACCESS_SECRET_KEY, algorithms=ALGORITHMS
        )
        user_id = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid access token")

    # 토큰 만료
    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Access token is expired")

    # 토큰 자체에 문제가 있는 경우(위조 등)
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid access token")

    return payload


# 리프레시 토큰 유효성 확인
def verify_refresh_token(refresh_token: str):

    try:
        payload = jwt.decode(
            token=refresh_token, key=REFRESH_SECRET_KEY, algorithms=ALGORITHMS
        )
        user_id = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid refresh token")

    # 토큰 만료
    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Refresh token is expired")

    # 토큰 자체에 문제가 있는 경우(위조 등)
    except JWTError:
        raise HTTPException(status_code=401, detail=f"JWT Error: {str(JWTError)}")

    return payload
