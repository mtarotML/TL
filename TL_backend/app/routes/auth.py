from fastapi import APIRouter, Depends, HTTPException, Body
from sqlmodel import Session, select
from ..database import engine
from ..models import User, Profile
from ..core.security import verify_password, create_access_token
from pydantic import BaseModel

router = APIRouter(prefix="/auth", tags=["auth"])

class LoginRequest(BaseModel):
    email: str
    password: str

def get_session():
    with Session(engine) as session:
        yield session

@router.post("/login")
def login(login_data: LoginRequest = Body(...), session: Session = Depends(get_session)):
    user = session.exec(select(User).where(User.email == login_data.email)).first()
    if not user or not verify_password(login_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    # Vérifier si le profil existe et est complété
    profile = session.exec(select(Profile).where(Profile.user_id == user.id)).first()
    profile_completed = profile.is_completed if profile else False

    token = create_access_token({"sub": str(user.id)})
    return {
        "access_token": token, 
        "token_type": "bearer", 
        "username": user.username,
        "user_id": user.id,
        "profile_completed": profile_completed
    }