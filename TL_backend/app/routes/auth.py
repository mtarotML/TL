from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from ..database import engine
from ..models import User
from ..core.security import verify_password, create_access_token

router = APIRouter(prefix="/auth", tags=["auth"])

def get_session():
    with Session(engine) as session:
        yield session

@router.post("/login")
def login(email: str, password: str, session: Session = Depends(get_session)):
    user = session.exec(select(User).where(User.email == email)).first()
    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    token = create_access_token({"sub": str(user.id)})
    return {"access_token": token, "token_type": "bearer", "username": user.username}
