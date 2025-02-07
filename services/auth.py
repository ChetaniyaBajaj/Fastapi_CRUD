from datetime import datetime, timedelta
from jose import jwt, JWTError
from passlib.context import CryptContext
import os
from fastapi import HTTPException, Depends, Header
from sqlalchemy.orm import Session
from database.database import SessionLocal
from models.contact_model import User

SECRET_KEY = os.getenv("SECRET_KEY", "default_secret_key")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def verify_token(authorization: str = Header(None)):
    """Extract and verify JWT token from Authorization header"""
    if not authorization:
        raise HTTPException(status_code=401, detail="Authorization header missing")

    try:
        scheme, token = authorization.split()
        if scheme.lower() != "bearer":
            raise HTTPException(status_code=401, detail="Invalid authentication scheme")

        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if not username:
            raise HTTPException(status_code=401, detail="Invalid token: No username found")

        return username  # Return authenticated username
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    except ValueError:
        raise HTTPException(status_code=401, detail="Invalid token format")

def get_current_user(db: Session = Depends(get_db), username: str = Depends(verify_token)):
    """Fetch the authenticated user from the database"""
    user = db.query(User).filter(User.username == username).first()
    if user is None:
        raise HTTPException(status_code=401, detail="User not found")
    return user