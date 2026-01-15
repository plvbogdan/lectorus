from pydantic import BaseModel, Field
import datetime
class UserCreate(BaseModel):
    email: str = Field(..., min_length=1, max_length=100)
    firstname: str = Field(..., min_length=1, max_length=100)
    lastname: str = Field(..., min_length=1, max_length=100)
    group: str = Field(..., min_length=1, max_length=100)
    password: str = Field(..., min_length=8)

class UserResponse(BaseModel):
    email: str = Field(..., min_length=1, max_length=100)
    firstname: str = Field(..., min_length=1, max_length=100)
    lastname: str = Field(..., min_length=1, max_length=100)
    group: str = Field(..., min_length=1, max_length=100)
    password: str = Field(..., min_length=8)

class LectureCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    topic: str = Field(..., min_length=1, max_length=100)

class LectureCreateResponse(BaseModel):
    id: int = Field(...)
    name: str = Field(..., min_length=1, max_length=100)
    group: str = Field(..., min_length=1, max_length=100)
    author_firstname: str = Field(..., min_length=1, max_length=100)
    author_lastname: str = Field(..., min_length=1, max_length=100)
    topic: str = Field(..., min_length=1, max_length=100)
    created_at: datetime = Field(...)
