from app.models.base import Base
from pydantic import BaseModel, Field



class CommentCreate(BaseModel):
    content: Annotated[str, Field(min_length=10, max_length=100)]

class CommentResponse(BaseModel):
    pass

class CommentDelete(BaseModel):
    pass

