from app.auth.dependencies import get_current_user
from app.auth.jwt import create_access_token
from app.auth.security import hash_password, verify_password
from app.database import get_db
from app.models.user import User
from app.schemas.auth import LoginRequest, RegisterRequest, TokenResponse, UpdateProfile, UserProfile
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/login", response_model=TokenResponse)
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == payload.email).first()

    if not user or not verify_password(payload.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"sub": user.id})
    return {"access_token": token}

@router.post("/register", response_model=TokenResponse)
def register(payload: RegisterRequest, db: Session = Depends(get_db)):
    if db.query(User).filter(User.email == payload.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")

    user = User(
        email=payload.email,
        name=payload.name,
        hashed_password=hash_password(payload.password)
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    token = create_access_token({"sub": user.id})
    return {"access_token": token}

@router.get("/me", response_model=UserProfile)
def get_profile(user: User = Depends(get_current_user)):
    return user

@router.put("/me", response_model=UserProfile)
def update_profile(
    payload: UpdateProfile,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if payload.name is not None:
        user.name = payload.name
    if payload.weight_unit is not None:
        if payload.weight_unit not in ['lbs', 'kg']:
            raise HTTPException(status_code=400, detail="weight_unit must be 'lbs' or 'kg'")
        user.weight_unit = payload.weight_unit
    
    db.commit()
    db.refresh(user)
    return user
