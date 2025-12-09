from app.schema.base_response import BaseResponse
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.schema.image_schema import (
    ImageVersionCreate,
    ImageCollectionCreate,
    ImageById,
    ImageList,
    ImageVersionResponse,
    ImageGenerationRequest,
    ImageGenerationList
)
from app.service.image_service import ImageService
from app.service.user_service import UserService
from app.ai.openai_image import generate_openai_image
from app.ai.hugging_face import generate_huggingface_image
from app.model.user_model import User

router = APIRouter(prefix="/images", tags=["Image collection"])


@router.post("/", response_model=BaseResponse[ImageById])
def create_collection(
    data: ImageCollectionCreate,
    db: Session = Depends(get_db),
    current_user = Depends(UserService.get_current_user)
):
    user = db.query(User).filter(User.email == current_user.email)
    if not user:
        raise HTTPException(status_code=403, detail="User not founded : Image Create collection")
    create_image = ImageService.create_image_collection(db, data, user_id=user["id"])
    
    if not create_image:
        raise HTTPException(status_code=400, detail="Failed to create image collection..")
    
    return BaseResponse(
        status=200,
        success=True,
        message="Create image collection",
        data=ImageById.from_orm(create_image)
    )
    
@router.post("/generate", response_model=BaseResponse[ImageGenerationList])
def generate_images(data: ImageGenerationRequest, current_user=Depends(UserService.get_current_user)):
    model = data.model.lower()
    
    if model == "openai":
        urls = generate_openai_image(prompt=data.prompt, style=data.style)
    elif model == "huggingface":
        urls = generate_huggingface_image(prompt=data.prompt, style=data.style)
    else :
        raise HTTPException(status_code=400, detail="Unsupported model")
    
    return BaseResponse(
        status=200,
        success=True,
        message=f"Images generate using {model}",
        data=ImageGenerationList.from_orm(urls) 
    )
    
@router.post("/{collecton_id}/version", response_model=BaseResponse[ImageVersionResponse])
def add_image_verson(
    collection_id: int,
    data: ImageVersionCreate,
    db: Session =Depends(get_db),
    current_user = Depends(UserService.get_current_user)
):
    new_version = ImageService.add_version(
        db=db,
        collection_id=collection_id,
        image_url=data.image_url,
        isFinal=data.isFinal
    )
    
    if not new_version:
        raise HTTPException(status_code=404, detail="Collection not founded!")
    
    return BaseResponse(
        status=200,
        success=True,
        message=f"New version added",
        data=ImageVersionResponse.from_orm(new_version)
    )
    
