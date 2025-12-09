import uuid
from imagekitio import ImageKit
from app.config.settings import settings
from fastapi import HTTPException

image_kit =ImageKit(
    private_key = settings.IMAGEKIT_PRIVATE_TOKEN,
    public_key = settings.IMAGEKIT_PUBLIC_TOKEN,
    url_endpoint = settings.IMAGEKIT_URL_ENDPOINT
)

def upload_image_to_imagekit(image_bytes: bytes, filename: str) -> str:
    result = image_kit.upload(
        file=image_bytes,
        file_name=filename
    )
    if not result or not result.url:
        raise HTTPException(status_code=401, detail="Image kit uploading error")
    
    return result.url