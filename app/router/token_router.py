from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from app.utils.jwt import create_access_token, create_refresh_token, verify_token
from datetime import timedelta
from app.schema.base_response import BaseResponse

router = APIRouter(prefix="/token", tags=["Users"])

class RefreshResponse(BaseModel):
    refresh_token: str
    
@router.post("/refresh", response_model=BaseResponse)
def refresh_token(data:RefreshResponse):
    token_data = verify_token(data.refresh_token, token_type="refresh")
    
    if not token_data:
        raise HTTPException(status_code=401, detail="Invailed refresh token!")
        # return BaseResponse(
        #     status=401, success=False, message="Invailed refresh token!", data=None
        # )
    
    new_access = create_access_token(token_data.email, token_data.phone)
    return BaseResponse(
        status=200,
        success=True,
        message="Token refreshed",
        data={"access_token": new_access}
    )
