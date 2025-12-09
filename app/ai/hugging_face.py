import requests
import uuid
from app.config.settings import settings
from fastapi import HTTPException
from app.service.imagekit_service import upload_image_to_imagekit
hf_token = settings.HUGGING_FACE_TOKEN
from huggingface_hub import InferenceClient

client = InferenceClient(
    provider="nebius",
    api_key=settings.HUGGING_FACE_TOKEN,
)

def generate_huggingface_image(prompt: str, style: str|None = None):
    full_prompt = f"{prompt},{style}" if style else prompt
    
    API_URL = "https://router.huggingface.co/models/CompVis/stable-diffusion-v1-4"
    headers = {"Authorization":f"Bearer {hf_token}"}
    
    
    response = requests.post(API_URL, headers=headers, json={"inputs":full_prompt})
    print(f"======== hugging face response ============ ", response)
    
    if response.status_code != 200:
        raise HTTPException(status_code=400, detail=f"Hugging face request failed! {response.text}")
    
    image_bytes = response.content
    
    prompt_clean = prompt.replace(" ", "_")[:40]
    unique_id = str(uuid.uuid4())[:8]
    filename = f"{prompt_clean}_{unique_id}.png"
    
    imagekit_url = upload_image_to_imagekit(image_bytes, filename)
    print(f"======= image kit hugging face =============== ", imagekit_url)
    return imagekit_url

def black_forest_labs_FLUX_1_dev(prompt: str, style: str|None = None):
    full_prompt = f"{prompt},{style}" if style else prompt
    response = client.text_to_image(
        full_prompt,
        model="black-forest-labs/FLUX.1-dev"
    )
    