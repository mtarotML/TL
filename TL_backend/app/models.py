from typing import Optional
from sqlmodel import SQLModel, Field, Relationship
from pydantic import BaseModel, EmailStr

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str
    email: str
    hashed_password: str
    
    # Relation avec Profile
    profile: Optional["Profile"] = Relationship(back_populates="user")

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

class Profile(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id", unique=True)
    
    # Informations de profil
    age: Optional[int] = None
    bio: Optional[str] = None
    city: Optional[str] = None
    photo_url: Optional[str] = None
    gender: Optional[str] = None  # "homme", "femme", "autre"
    looking_for: Optional[str] = None  # "homme", "femme", "tous"
    
    # Flag pour savoir si le profil est complété
    is_completed: bool = Field(default=False)
    
    # Relation avec User
    user: Optional[User] = Relationship(back_populates="profile")

class ProfileCreate(BaseModel):
    age: int
    bio: str
    city: str
    photo_url: Optional[str] = None
    gender: str
    looking_for: str

class ProfileUpdate(BaseModel):
    age: Optional[int] = None
    bio: Optional[str] = None
    city: Optional[str] = None
    photo_url: Optional[str] = None
    gender: Optional[str] = None
    looking_for: Optional[str] = None