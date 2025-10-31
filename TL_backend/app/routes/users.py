from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import Session
from ..database import engine
from ..models import User, UserCreate
from ..core.security import hash_password
from sqlmodel import select

router = APIRouter(prefix="/users", tags=["users"])

def get_session():
    with Session(engine) as session:
        yield session

@router.post("/register")
def register(user_data: UserCreate, session: Session = Depends(get_session)):
    statement = select(User).where(User.email == user_data.email)
    existing_user = session.exec(statement).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    print("\nLe mot de passe ressemble a ca :",user_data.password)
    print("\nle type du mdp est :",type(user_data.password))
    hashed_pw = hash_password(user_data.password)
    new_user = User(username=user_data.username, email=user_data.email, hashed_password=hashed_pw)
    session.add(new_user)
    session.commit()
    session.refresh(new_user)

    return {"message": "User created successfully", "user_id": new_user.id}
