from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.security import create_access_token, get_password_hash, verify_password
from app.db.session import get_db
from app.models import User
from app.schemas.schemas import Token, UserCreate, UserLogin
router = APIRouter(prefix="/auth", tags=["auth"])
@router.post("/register", response_model=Token)
def register(payload: UserCreate, db: Session = Depends(get_db)):
    if db.query(User).filter(User.email == payload.email).first(): raise HTTPException(409, "Email already registered")
    user = User(email=payload.email, full_name=payload.full_name, hashed_password=get_password_hash(payload.password)); db.add(user); db.commit(); db.refresh(user)
    return {"access_token": create_access_token(str(user.id)), "user": user}
@router.post("/login", response_model=Token)
def login(payload: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == payload.email).first()
    if not user or not verify_password(payload.password, user.hashed_password): raise HTTPException(401, "Invalid email or password")
    return {"access_token": create_access_token(str(user.id)), "user": user}
