from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from pathlib import Path
import uuid
import base64
from io import BytesIO
import logging

from core.model_manager import model_manager
from core.gpu_monitor import gpu_monitor
from models.database import Database
from config import settings

logger = logging.getLogger(__name__)
router = APIRouter()

# Initialize database
db = Database(settings.DB_PATH)

# Request Models
class GenerateImageRequest(BaseModel):
    prompt: str = Field(..., min_length=1, max_length=1000)
    negative_prompt: str = ""
    width: int = Field(default=512, ge=64, le=2048)
    height: int = Field(default=512, ge=64, le=2048)
    num_inference_steps: int = Field(default=30, ge=1, le=150)
    guidance_scale: float = Field(default=7.5, ge=0.0, le=20.0)
    num_images: int = Field(default=1, ge=1, le=4)
    seed: Optional[int] = None

class LoadModelRequest(BaseModel):
    model_config = {"protected_namespaces": ()}
    
    model_key: str

# API Routes
@router.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": settings.APP_VERSION
    }

@router.get("/gpu/info")
async def get_gpu_info():
    """Get GPU information and stats"""
    return gpu_monitor.get_gpu_info()

@router.post("/gpu/clear-cache")
async def clear_gpu_cache():
    """Clear GPU cache"""
    gpu_monitor.clear_cache()
    return {"success": True, "message": "GPU cache cleared"}

@router.get("/models")
async def list_models():
    """List all available models"""
    return model_manager.list_available_models()

@router.get("/models/current")
async def get_current_model():
    """Get currently loaded model info"""
    return model_manager.get_current_model_info()

@router.post("/models/load")
async def load_model(request: LoadModelRequest):
    """Load a specific model"""
    result = model_manager.load_model(request.model_key)
    if not result["success"]:
        raise HTTPException(status_code=400, detail=result["error"])
    return result

@router.post("/generate/image")
async def generate_image(request: GenerateImageRequest, background_tasks: BackgroundTasks):
    """Generate images from text prompt"""
    try:
        # Check if model is loaded
        if model_manager.pipeline is None:
            # Auto-load default model
            logger.info("No model loaded, loading default model...")
            load_result = model_manager.load_model("sdxl-turbo")
            if not load_result["success"]:
                raise HTTPException(status_code=400, detail="Failed to load model")
        
        # Generate images
        result = model_manager.generate_image(
            prompt=request.prompt,
            negative_prompt=request.negative_prompt,
            width=request.width,
            height=request.height,
            num_inference_steps=request.num_inference_steps,
            guidance_scale=request.guidance_scale,
            num_images=request.num_images,
            seed=request.seed
        )
        
        if not result["success"]:
            raise HTTPException(status_code=500, detail=result["error"])
        
        # Save images to disk
        images_data = []
        for idx, image in enumerate(result["images"]):
            # Generate unique filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{timestamp}_{uuid.uuid4().hex[:8]}_{idx}.png"
            file_path = settings.OUTPUTS_DIR / filename
            
            # Save image
            image.save(file_path)
            
            # Convert to base64 for response
            buffered = BytesIO()
            image.save(buffered, format="PNG")
            img_str = base64.b64encode(buffered.getvalue()).decode()
            
            # Save to database in background
            background_tasks.add_task(
                db.save_generation,
                prompt=request.prompt,
                negative_prompt=request.negative_prompt,
                model_key=model_manager.current_model,
                width=request.width,
                height=request.height,
                steps=request.num_inference_steps,
                guidance_scale=request.guidance_scale,
                seed=request.seed,
                file_path=str(file_path)
            )
            
            images_data.append({
                "filename": filename,
                "path": str(file_path),
                "base64": img_str
            })
        
        return {
            "success": True,
            "images": images_data,
            "count": len(images_data),
            "prompt": request.prompt,
            "model": model_manager.current_model
        }
        
    except Exception as e:
        logger.error(f"Generation error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/history")
async def get_history(limit: int = 50):
    """Get generation history"""
    try:
        generations = await db.get_recent_generations(limit)
        return {"generations": generations, "count": len(generations)}
    except Exception as e:
        logger.error(f"Error fetching history: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/history/{gen_id}")
async def get_generation(gen_id: int):
    """Get specific generation"""
    generation = await db.get_generation_by_id(gen_id)
    if not generation:
        raise HTTPException(status_code=404, detail="Generation not found")
    return generation

@router.delete("/history/{gen_id}")
async def delete_generation(gen_id: int):
    """Delete generation"""
    success = await db.delete_generation(gen_id)
    if not success:
        raise HTTPException(status_code=404, detail="Generation not found")
    return {"success": True}

@router.get("/history/search")
async def search_history(q: str, limit: int = 50):
    """Search generation history"""
    try:
        generations = await db.search_generations(q, limit)
        return {"generations": generations, "count": len(generations)}
    except Exception as e:
        logger.error(f"Error searching history: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/stats")
async def get_stats():
    """Get generation statistics"""
    try:
        stats = await db.get_stats()
        gpu_info = gpu_monitor.get_gpu_info()
        return {
            "stats": stats,
            "gpu": gpu_info
        }
    except Exception as e:
        logger.error(f"Error fetching stats: {e}")
        raise HTTPException(status_code=500, detail=str(e))
