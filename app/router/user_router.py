from app.schema.base_response import BaseResponse
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.schema.user_schema import Token
from app.schema.user_schema import createUser, UserById, UserList, LoginRequest
from app.service.user_service import UserService
from fastapi.security import OAuth2PasswordRequestForm
from app.utils.jwt import create_access_token, create_refresh_token

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/register", response_model=BaseResponse[UserById])
def create_user(data: createUser, db: Session = Depends(get_db)):
    user = UserService.create_user(db, data)
    if not user:
        HTTPException(status_code=401, detail="Create user error!")
        return BaseResponse(
            status=401, success=False, message="Create user error", data=None
        )

    return BaseResponse(
        status=200,
        success=True,
        message="User created successfully",
        data=UserById.from_orm(user),  # ? is filter user to userbyid?
    )


@router.get("/{user_id}", response_model=BaseResponse[UserById])
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = UserService.get_by_id(db, user_id)
    print(f"========= users ========== ", user, user_id)
    if not user:
        HTTPException(status_code=404, detail="User not founded")
        return BaseResponse(
            status=404, success=False, message="User not founded", data=None
        )
    return BaseResponse(
        status=200, success=True, message="User fetched", data=UserById.from_orm(user)
    )


@router.get("/", response_model=BaseResponse[UserList])
def get_all(db: Session = Depends(get_db)):
    users = UserService.get_all(db)

    user_list = [UserById.from_orm(user) for user in users]
    # print(f"========= users ========== ", user_list)
    return BaseResponse(
        status=200,
        success=True,
        message="Users fetched successfully",
        data=UserList(users=user_list),
    )


@router.post("/login", response_model=BaseResponse[Token])
def login(data: LoginRequest, db: Session = Depends(get_db)):
    print(" ========= router ========= ", data.password, data.email)
    user = UserService.authenticate_user(db, data.email, data.password)

    if not user:
        raise HTTPException(status_code=401, detail="Invalid user login")
        # return BaseResponse(
        #     status=401, success=False, message="Invalid user login!", data=None
        # )

    access_token = create_access_token(user.email, user.phone)
    refresh_token = create_refresh_token(user.email, user.phone)
    
    if refresh_token and access_token:
        return BaseResponse(
            status=200,
            success=True,
            message="Token generate successfully",
            data=Token(access_token=access_token, refresh_token=refresh_token),
        )
