import os

from dotenv import load_dotenv

load_dotenv()

INSTANCE_DIR = os.path.join(os.path.dirname(__file__), "..", "instance")
os.makedirs(INSTANCE_DIR, exist_ok=True)


class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
