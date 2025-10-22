from typing import Optional
from sqlmodel import SQLModel, Field
from pydantic import BaseModel, EmailStr

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str
    email: str
    hashed_password: str
class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str