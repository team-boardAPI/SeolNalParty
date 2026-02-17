import os
from dotenv import load_dotenv

# .env 파일이 없어도 무시하고 넘어갑니다.
load_dotenv()

class Config:
    # 💡 핵심: os.getenv의 두 번째 인자로 기본 주소를 넣습니다.
    # 환경 변수(DATABASE_URL)가 없으면 자동으로 sqlite 주소를 사용합니다.
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///./seolnal_party.db")

# 확인용 (서버 켤 때 터미널에 주소가 찍힙니다)
print(f"Connecting to: {Config.SQLALCHEMY_DATABASE_URI}")