from pydantic import BaseModel
from typing import List
from datetime import datetime


class createUser(BaseModel):
    phone: str
    email: str
    address: str | None = None
    name: str | None = None
    password: str
    
    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "examples": [
                {
                    "name": "user1",
                    "email": "user1@gmail.com",
                    "address": "address1",
                    "phone": "12345678901",
                    "password": "12345678"
                }
            ]
        },
    }


# worked when router send response.


class UserById(BaseModel):
    id: int
    phone: str
    email: str
    address: str | None = None
    name: str | None = None

    created_at: datetime
    updated_at: datetime

    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "examples": [
                {
                    # "user_id": 1,
                    "name": "user1",
                    "email": "user1@gmail.com",
                    "address": "address1",
                    "phone": "12345678901",
                }
            ]
        },
    }


class UserList(BaseModel):
    users: List[UserById] | None = None


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    email: str | None = None
    phone: str | None = None


class LoginRequest(BaseModel):
    email: str | None = None
    password: str | None = None
    
    model_config= {
        "from_attributes": True,
        "json_schema_extra":{
            "examples":[
                {
                    "email": "user1@gmail.com",
                    "password": "secret123"
                }
            ]
        }
    }
