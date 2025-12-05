from pydantic import BaseModel
from typing import List
from datetime import datetime


class ImageVersionCreate(BaseModel):
    image_url: str
    isFinal: bool = False

class ImageCollectionCreate(BaseModel):
    prompt: str
    model: str
    style: str
    image_version: List[ImageVersionCreate]
    
    
# class ImageCollectionList(BaseModel):

class ImageList(BaseModel):
    images: List[ImageById] | None = None
    
class ImageGenerationRequest(BaseModel):
    prompt: str
    style: str | None = None
    model: str

class ImageGenerationList(BaseModel):
    urls: List[str] 
    
class ImageVersionResponse(BaseModel):
    id: int
    image_url: str
    isFinal: bool
    prarent_id: int
    
    collection_id: int
    
    created_at: datetime
    updated_at: datetime
    
    model_config= {
        "from_attributes": True,
    }
    
    
class ImageById(BaseModel):
    id: int
    prompt: str
    model: str
    style: str
    user_id: int
    image_version: List[ImageVersionResponse]
    
    created_at: datetime
    updated_at: datetime
    
    
    model_config= {
        "from_attributes": True,
        "json_schema_extra": {
            "examples": [
                {
                    # "user_id": 1,
                    "prompt": "Generate a cat image",
                    "model": "huggingFace",
                    "style": "surprise me",
                    "user_id": 4,
                    "image_version": [
                        {
                           "id": 10,
                           "image_url": "https://example.com/img1.png",
                           "parent_id": 1,
                           "isFinal": False,
                            "created_at": "2025-12-02T16:09:17.768648",
                            "updated_at": "2025-12-02T16:09:17.768648"
                        }
                    ],
                    "created_at": "2025-12-02T16:09:17.768648",
                    "updated_at": "2025-12-02T16:09:17.768648"
                }
            ]
        },
    }
    