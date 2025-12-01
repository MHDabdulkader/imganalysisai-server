from pydantic import BaseModel

class ImageCollectionCreate(BaseModel):
    prompt: str
    model: str
    image_url: str
    user_id : int
    
class ImageCollectionList(BaseModel):
    