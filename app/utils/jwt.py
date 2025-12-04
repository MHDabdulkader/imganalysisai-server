import jwt
from jwt.exceptions import InvalidTokenError
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from app.schema.user_schema import TokenData
from pydantic import BaseModel
from datetime import datetime, timezone, timedelta
from app.config.settings import settings
from typing import List

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login")

def create_access_token(email: str | None, phone: str | None) -> str | None:
    if not (email and phone):
        return None
    
    payload = {
        "sub": f"{email}:{phone}",
        "type": "access",
        "exp": datetime.now(timezone.utc) + timedelta(minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
    }    
    
    return jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)

def create_refresh_token(email: str|None, phone: str|None) -> str | None:
    if not (email and phone):
        return None
    payload = {
        "sub": f"{email}:{phone}",
        "type": "refresh",
        "exp": datetime.now(timezone.utc) + timedelta(minutes=settings.JWT_REFRESH_TOKEN_EXPIRE_DAYS)
    }    
    
    return jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)


def verify_token(token: str, token_type: str = "access") -> TokenData | None:
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        
        if payload.get("type") != token_type:
            return None
        email, phone = payload["sub"].split(":")
        return TokenData(email=email, phone=phone)
    except jwt.PyJWKError:
        return None

def extract_users(token: str, token_type:str = "access") ->str| None:
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        
        if payload.get("type") != token_type:
            return None
        
        email = payload["sub"].split(":")
        return email
    except jwt.PyJWKError:
        return None
    
    
