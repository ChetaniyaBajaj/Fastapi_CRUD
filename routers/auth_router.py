from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from services.auth import get_db, hash_password, verify_password, create_access_token
from schemas.contact_schema import UserCreate, UserLogin
from models.contact_model import User

router = APIRouter(tags=["Authentication"])

@router.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.username == user.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")

    new_user = User(username=user.username, password=hash_password(user.password))
    db.add(new_user)
    db.commit()
    return {"message": "User registered successfully"}

@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == user.username).first()
    if not db_user or not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"sub": db_user.username})
    return {"access_token": token, "token_type": "bearer"}
