import openai
from fastapi import HTTPException
import base64
from app.service.imagekit_service import upload_image_to_imagekit
from app.config.settings import settings

openai.api_key = settings.OPENAI_API_KEY


def generate_openai_image(prompt: str, style: str|None = None):
    full_prompt = f"{prompt},{style}" if style else prompt
    print("====== full prompt openai ============ ", full_prompt)
    
    response = openai.images.generate(
        model="gpt-image-1",
        prompt=full_prompt,
        size="1024x1024",
        n=1
    )
    
    urls =[]
    if not response or not response.data:
        raise HTTPException(status_code=400, detail="open ai response error!")
    
    for idx, item in enumerate(response.data):
        image_base64 = item.b64_json
        if image_base64 is None:
            raise HTTPException(status_code=400, detail="Failed to generate image!")
        
        image_bytes = base64.b64decode(image_base64)
        filename = f"{prompt.replace(" ", "_")}_{idx+1}.png"
        
        imagekit_url = upload_image_to_imagekit(image_bytes, filename)
        
        urls.append(imagekit_url)
        
    return urls