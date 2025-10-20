from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class GenerationBase(BaseModel):
    prompt: str
    negative_prompt: Optional[str] = None
    model_key: str
    width: int
    height: int
    steps: int
    guidance_scale: float
    seed: Optional[int] = None

class GenerationCreate(GenerationBase):
    file_path: str
    thumbnail_path: Optional[str] = None

class GenerationResponse(GenerationBase):
    id: int
    file_path: str
    thumbnail_path: Optional[str] = None
    created_at: datetime
    
    class Config:
        from_attributes = True
