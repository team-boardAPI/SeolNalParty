from pydantic import BaseModel, EmailStr, Field


class CreateUser(BaseModel):
    login_id: str = Field(min_length=4, max_length=15)
    user_name: str = Field(min_length=1, max_length=100)
    email: EmailStr
    password: str = Field(min_length=4)


class LoginSchema(BaseModel):
    login_id: str = Field(min_length=4, max_length=15)
    password: str


class RefreshToken(BaseModel):
    refresh_token: str


class LogoutSchema(BaseModel):
    access_token: str
    refresh_token: str
