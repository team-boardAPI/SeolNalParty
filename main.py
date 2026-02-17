import uvicorn
# 2. 데이터베이스 테이블 생성을 위한 모듈 가져오기
from core.database import Base, engine
from fastapi import FastAPI
# 1. 우리가 만든 라우터 가져오기
from routers import posts

# 3. DB 테이블 자동 생성
# 서버가 시작될 때, 모델(Post, User, Like 등)에 정의된 테이블이 DB에 없으면 자동으로 만들어줍니다.
Base.metadata.create_all(bind=engine)

# 4. FastAPI 앱 인스턴스 생성
app = FastAPI(
    title="나만의 게시판 API",
    description="FastAPI와 SQLAlchemy로 만든 게시판 프로젝트입니다.",
    version="1.0.0",
)

# 5. 라우터 등록
# 이제 http://localhost:8000/posts/... 주소로 요청이 오면 posts 라우터가 처리합니다.
app.include_router(posts.router)


# 6. 기본 루트 경로 확인용
@app.get("/")
def read_root():
    return {"message": "Hello! 게시판 서버가 정상적으로 실행 중입니다. 🚀"}


# (옵션) 파이썬 스크립트로 직접 실행할 때 필요 (python main.py)
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
