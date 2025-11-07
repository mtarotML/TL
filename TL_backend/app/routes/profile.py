from fastapi import APIRouter, HTTPException, Depends, Header
from sqlmodel import Session, select
from ..database import engine
from ..models import Profile, ProfileCreate, ProfileUpdate, User
from ..core.security import verify_token
from typing import Optional

router = APIRouter(prefix="/profile", tags=["profile"])

def get_session():
    with Session(engine) as session:
        yield session

def get_current_user_id(authorization: Optional[str] = Header(None)) -> int:
    """Extrait l'user_id depuis le token JWT dans le header Authorization"""
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Token manquant ou invalide")
    
    token = authorization.replace("Bearer ", "")
    user_id = verify_token(token)
    if not user_id:
        raise HTTPException(status_code=401, detail="Token invalide ou expiré")
    
    return user_id

@router.get("/me")
def get_my_profile(
    user_id: int = Depends(get_current_user_id),
    session: Session = Depends(get_session)
):
    """Récupère le profil de l'utilisateur connecté"""
    profile = session.exec(
        select(Profile).where(Profile.user_id == user_id)
    ).first()
    
    if not profile:
        return {"profile_exists": False, "message": "Profil non créé"}
    
    return {
        "profile_exists": True,
        "profile": profile
    }

@router.post("/create")
def create_profile(
    profile_data: ProfileCreate,
    user_id: int = Depends(get_current_user_id),
    session: Session = Depends(get_session)
):
    """Crée le profil de l'utilisateur (première connexion)"""
    # Vérifier si le profil existe déjà
    existing_profile = session.exec(
        select(Profile).where(Profile.user_id == user_id)
    ).first()
    
    if existing_profile:
        raise HTTPException(status_code=400, detail="Profil déjà existant")
    
    # Créer le profil
    new_profile = Profile(
        user_id=user_id,
        age=profile_data.age,
        bio=profile_data.bio,
        city=profile_data.city,
        photo_url=profile_data.photo_url,
        gender=profile_data.gender,
        looking_for=profile_data.looking_for,
        is_completed=True
    )
    
    session.add(new_profile)
    session.commit()
    session.refresh(new_profile)
    
    return {"message": "Profil créé avec succès", "profile": new_profile}

@router.put("/update")
def update_profile(
    profile_data: ProfileUpdate,
    user_id: int = Depends(get_current_user_id),
    session: Session = Depends(get_session)
):
    """Met à jour le profil de l'utilisateur"""
    profile = session.exec(
        select(Profile).where(Profile.user_id == user_id)
    ).first()
    
    if not profile:
        raise HTTPException(status_code=404, detail="Profil non trouvé")
    
    # Mise à jour des champs fournis
    update_data = profile_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(profile, key, value)
    
    # Marquer comme complété si au moins les champs de base sont remplis
    if profile.age and profile.bio and profile.city and profile.gender and profile.looking_for:
        profile.is_completed = True
    
    session.add(profile)
    session.commit()
    session.refresh(profile)
    
    return {"message": "Profil mis à jour avec succès", "profile": profile}

@router.get("/{user_id}")
def get_user_profile(
    user_id: int,
    current_user_id: int = Depends(get_current_user_id),
    session: Session = Depends(get_session)
):
    """Récupère le profil d'un autre utilisateur (pour le matching plus tard)"""
    profile = session.exec(
        select(Profile).where(Profile.user_id == user_id)
    ).first()
    
    if not profile:
        raise HTTPException(status_code=404, detail="Profil non trouvé")
    
    if not profile.is_completed:
        raise HTTPException(status_code=403, detail="Profil non complété")
    
    # Récupérer aussi le username
    user = session.exec(select(User).where(User.id == user_id)).first()
    
    return {
        "username": user.username if user else None,
        "profile": profile
    }