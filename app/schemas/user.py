from pydantic import BaseModel, EmailStr, Field


class UpdateUser(BaseModel):
    user_name: str = Field(min_length=1, max_length=100)
    password: str = Field(min_length=4)


class UserInfo(BaseModel):
    user_id: int
    login_id: str
    user_name: str
    email: EmailStr
    password: str

    model_config = {"from_attributes": True}


class UserDelete(BaseModel):
    message: str
