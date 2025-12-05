from sqlalchemy.orm import Session
from app.model.user_model import User
from app.schema.user_schema import createUser
from app.utils.bcrypt import hash_password, password_verify
from app.utils.jwt import verify_token
from fastapi import Header, HTTPException
from app.schema.base_response import BaseResponse

class UserService:
    @staticmethod
    def create_user( db: Session, data: createUser):
        hashPass = hash_password(data.password)
        print(" =============== create user data ================ ", createUser)
        newUser = User(
            phone= data.phone,
            email = data.email,
            address = data.address,
            name = data.name,
            password = hashPass
        )
        
        db.add(newUser)
        db.commit()
        
        db.refresh(newUser)
        
        return newUser

    @staticmethod
    def get_by_id(db: Session, user_id: int):
        response_query = db.query(User).filter(User.id == user_id).first()
        # print(f"======== serive get by id ======= ", response_query, user_id)
        return response_query
    
    @staticmethod
    def get_all(db: Session):
        response_query = db.query(User).all()
        return response_query
    
    @staticmethod
    def authenticate_user(db: Session, email, password):
        user = db.query(User).filter(User.email == email).first()
        print("\n===================== user ============= ", user, email, password)
        if not user:
            return None
        # print("\n===================== user ============= ", user)
        isValid = password_verify(password, user.password)
        if isValid:
            return user
        return None
    
    @staticmethod
    def get_current_user(authorization: str = Header(...)):
        if not authorization:
            HTTPException(status_code=401, detail="Missing authorizaton..")
            return BaseResponse(status=401, success=False, message="Missing authorization..", data=None)
        
        try :
            scheme, token = authorization.split()
            if scheme.lower() != "bearer":
                HTTPException(status_code=401, detail="Invalid auth scheme..")
                return BaseResponse(status=401, success=False, message="Invalid auth scheme..", data=None)
        except ValueError:
            HTTPException(status_code=401, detail="Invalid auth header format..")
            return BaseResponse(status=401, success=False, message="Invalid auth header format..", data=None)
        
        try:
            payload = verify_token(token)
            return payload
        except Exception:
            HTTPException(status_code=401, detail="Invalid or expire token..")
            return BaseResponse(status=401, success=False, message="Invalid or expire token..", data=None)
    
    