from pydantic import BaseModel


class DiffusionInstructions(BaseModel):
    prompt: str
    negative_prompt: str = ""
    num_inference_steps: int = 28
    guidance_scale: float = 7.0


class ImageToImageInstructions(DiffusionInstructions):
    encoded_base_image: str


class TextToImageInstructions(DiffusionInstructions):
    width: int = 1024
    height: int = 1024


class Errand(BaseModel):
    instructions: TextToImageInstructions | ImageToImageInstructions
    origin: str
    destination: str
    identifier: str
    timestamp: float
