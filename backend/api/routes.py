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
    prompt: str = Field(..., min_length=1, max_length=2000)
    negative_prompt: str = ""
    width: int = Field(default=1024, ge=64, le=2048)
    height: int = Field(default=1024, ge=64, le=2048)
    num_inference_steps: int = Field(default=30, ge=1, le=150)
    guidance_scale: float = Field(default=7.5, ge=0.0, le=20.0)
    num_images: int = Field(default=1, ge=1, le=20)
    seed: Optional[int] = None
    scheduler: Optional[str] = None
    denoise_strength: Optional[float] = Field(default=0.75, ge=0.0, le=1.0)
    input_image: Optional[str] = None
    sampler: Optional[str] = None
    scheduler: Optional[str] = None

class LoadModelRequest(BaseModel):
    model_config = {"protected_namespaces": ()}
    
    model_key: str

class AddLoRARequest(BaseModel):
    model_config = {"protected_namespaces": ()}
    
    name: str = Field(..., min_length=1, max_length=200)
    file_path: str = Field(..., min_length=1)
    model_type: str = Field(..., min_length=1)
    trigger_words: Optional[str] = None
    description: Optional[str] = None
    weight: float = Field(default=1.0, ge=0.0, le=2.0)

class UpdateLoRARequest(BaseModel):
    name: Optional[str] = None
    trigger_words: Optional[str] = None
    description: Optional[str] = None
    weight: Optional[float] = Field(default=None, ge=0.0, le=2.0)

class SetLoRAActiveRequest(BaseModel):
    is_active: bool
    weight: Optional[float] = Field(default=None, ge=0.0, le=2.0)

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
        
        # Load active LoRAs into pipeline
        active_loras = await db.get_active_loras()
        if active_loras:
            logger.info(f"Loading {len(active_loras)} active LoRAs into pipeline...")
            lora_result = model_manager.load_loras(active_loras)
            if not lora_result["success"]:
                logger.warning(f"Failed to load LoRAs: {lora_result.get('error')}")
                # Don't fail generation, just warn
        
        # Generate images (txt2img or img2img)
        if request.input_image:
            # Image-to-Image generation
            result = model_manager.generate_img2img(
                prompt=request.prompt,
                negative_prompt=request.negative_prompt,
                input_image_base64=request.input_image,
                width=request.width,
                height=request.height,
                num_inference_steps=request.num_inference_steps,
                guidance_scale=request.guidance_scale,
                num_images=request.num_images,
                seed=request.seed,
                scheduler=request.scheduler,
                strength=request.denoise_strength
            )
        else:
            # Text-to-Image generation
            result = model_manager.generate_image(
                prompt=request.prompt,
                negative_prompt=request.negative_prompt,
                width=request.width,
                height=request.height,
                num_inference_steps=request.num_inference_steps,
                guidance_scale=request.guidance_scale,
                num_images=request.num_images,
                seed=request.seed,
                scheduler=request.scheduler
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
                file_path=str(file_path),
                scheduler=request.scheduler,
                denoise_strength=request.denoise_strength if request.input_image else None
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

# LoRA Management Endpoints
@router.post("/loras")
async def add_lora(request: AddLoRARequest):
    """Add a new LoRA"""
    try:
        # Verify file exists
        if not Path(request.file_path).exists():
            raise HTTPException(status_code=400, detail="LoRA file not found")
        
        lora_id = await db.add_lora(
            name=request.name,
            file_path=request.file_path,
            model_type=request.model_type,
            trigger_words=request.trigger_words,
            description=request.description,
            weight=request.weight
        )
        
        return {
            "success": True,
            "lora_id": lora_id,
            "message": "LoRA added successfully"
        }
    except Exception as e:
        logger.error(f"Error adding LoRA: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/loras")
async def list_loras(model_type: Optional[str] = None):
    """Get all LoRAs, optionally filtered by model type"""
    try:
        loras = await db.get_loras(model_type)
        return {"loras": loras, "count": len(loras)}
    except Exception as e:
        logger.error(f"Error listing LoRAs: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/loras/active")
async def get_active_loras():
    """Get all active LoRAs"""
    try:
        loras = await db.get_active_loras()
        return {"loras": loras, "count": len(loras)}
    except Exception as e:
        logger.error(f"Error getting active LoRAs: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.patch("/loras/{lora_id}")
async def update_lora(lora_id: int, request: UpdateLoRARequest):
    """Update LoRA details"""
    try:
        success = await db.update_lora(
            lora_id=lora_id,
            name=request.name,
            trigger_words=request.trigger_words,
            description=request.description,
            weight=request.weight
        )
        
        if not success:
            raise HTTPException(status_code=404, detail="LoRA not found or no changes made")
        
        return {"success": True, "message": "LoRA updated successfully"}
    except Exception as e:
        logger.error(f"Error updating LoRA: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.patch("/loras/{lora_id}/activate")
async def set_lora_active(lora_id: int, request: SetLoRAActiveRequest):
    """Activate or deactivate a LoRA"""
    try:
        # Update weight if provided
        if request.weight is not None:
            await db.update_lora(lora_id=lora_id, weight=request.weight)
        
        # Set active status
        success = await db.set_lora_active(lora_id, request.is_active)
        
        if not success:
            if request.is_active:
                raise HTTPException(status_code=400, detail="Maximum 5 LoRAs can be active at once")
            else:
                raise HTTPException(status_code=404, detail="LoRA not found")
        
        # Load/unload LoRA in model manager
        if request.is_active:
            active_loras = await db.get_active_loras()
            model_manager.load_loras(active_loras)
        else:
            active_loras = await db.get_active_loras()
            model_manager.load_loras(active_loras)
        
        return {
            "success": True,
            "message": f"LoRA {'activated' if request.is_active else 'deactivated'} successfully"
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error setting LoRA active status: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/loras/{lora_id}")
async def delete_lora(lora_id: int):
    """Delete a LoRA"""
    try:
        success = await db.delete_lora(lora_id)
        
        if not success:
            raise HTTPException(status_code=404, detail="LoRA not found")
        
        # Reload active LoRAs
        active_loras = await db.get_active_loras()
        model_manager.load_loras(active_loras)
        
        return {"success": True, "message": "LoRA deleted successfully"}
    except Exception as e:
        logger.error(f"Error deleting LoRA: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/loras/deactivate-all")
async def deactivate_all_loras():
    """Deactivate all LoRAs"""
    try:
        await db.deactivate_all_loras()
        model_manager.unload_all_loras()
        return {"success": True, "message": "All LoRAs deactivated"}
    except Exception as e:
        logger.error(f"Error deactivating all LoRAs: {e}")
        raise HTTPException(status_code=500, detail=str(e))
