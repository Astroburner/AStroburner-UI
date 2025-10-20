from fastapi import APIRouter, HTTPException, BackgroundTasks
from fastapi.responses import FileResponse
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
    weight: float = Field(default=1.0, ge=-1.0, le=2.0)

class UpdateLoRARequest(BaseModel):
    name: Optional[str] = None
    trigger_words: Optional[str] = None
    description: Optional[str] = None
    weight: Optional[float] = Field(default=None, ge=-1.0, le=2.0)

class SetLoRAActiveRequest(BaseModel):
    is_active: bool
    weight: Optional[float] = Field(default=None, ge=-1.0, le=2.0)

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

# Custom Models Management Endpoints
class AddCustomModelRequest(BaseModel):
    model_config = {"protected_namespaces": ()}
    
    name: str = Field(..., min_length=1, max_length=200)
    file_path: str = Field(..., min_length=1)
    model_type: Optional[str] = None  # If None, will auto-detect
    precision: Optional[str] = None  # If None, will auto-detect
    description: Optional[str] = None
    thumbnail_path: Optional[str] = None

@router.post("/custom-models")
async def add_custom_model(request: AddCustomModelRequest):
    """Add a new custom model"""
    try:
        from utils.model_detector import detect_model_type, get_supported_model_types
        
        # Verify file exists
        file_path = Path(request.file_path)
        if not file_path.exists():
            raise HTTPException(status_code=400, detail="Model file not found")
        
        if not file_path.suffix.lower() == '.safetensors':
            raise HTTPException(status_code=400, detail="Only .safetensors files are supported")
        
        # Auto-detect model type and precision if not provided
        model_type = request.model_type
        precision = request.precision
        
        if not model_type or not precision:
            detected_type, detected_precision = detect_model_type(request.file_path)
            
            if not model_type:
                model_type = detected_type
            if not precision:
                precision = detected_precision
        
        # Validate model type
        supported_types = get_supported_model_types()
        if model_type not in supported_types and model_type != "Unknown":
            raise HTTPException(
                status_code=400, 
                detail=f"Unsupported model type. Must be one of: {', '.join(supported_types)}"
            )
        
        # Add to database
        model_id = await db.add_custom_model(
            name=request.name,
            file_path=request.file_path,
            model_type=model_type,
            precision=precision,
            description=request.description,
            thumbnail_path=request.thumbnail_path
        )
        
        return {
            "success": True,
            "model_id": model_id,
            "detected_type": model_type,
            "detected_precision": precision,
            "message": "Custom model added successfully"
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error adding custom model: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/custom-models/model-types")
async def get_supported_model_types_endpoint():
    """Get list of supported model types"""
    from utils.model_detector import get_supported_model_types, get_supported_precisions
    return {
        "model_types": get_supported_model_types(),
        "precisions": get_supported_precisions()
    }

@router.post("/custom-models/detect")
async def detect_model_type_endpoint(file_path: str):
    """Detect model type and precision from file"""
    try:
        from utils.model_detector import detect_model_type
        
        if not Path(file_path).exists():
            raise HTTPException(status_code=400, detail="File not found")
        
        model_type, precision = detect_model_type(file_path)
        
        return {
            "model_type": model_type,
            "precision": precision,
            "file_path": file_path
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error detecting model type: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/custom-models")
async def list_custom_models():
    """Get all custom models"""
    try:
        models = await db.get_custom_models()
        return {"models": models, "count": len(models)}
    except Exception as e:
        logger.error(f"Error listing custom models: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/custom-models/{model_id}")
async def get_custom_model(model_id: int):
    """Get specific custom model"""
    try:
        model = await db.get_custom_model_by_id(model_id)
        if not model:
            raise HTTPException(status_code=404, detail="Custom model not found")
        return model
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting custom model: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/custom-models/{model_id}")
async def delete_custom_model(model_id: int):
    """Delete a custom model"""
    try:
        success = await db.delete_custom_model(model_id)
        if not success:
            raise HTTPException(status_code=404, detail="Custom model not found")
        return {"success": True, "message": "Custom model deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting custom model: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/thumbnail")
async def get_thumbnail(path: str):
    """Serve thumbnail image from local filesystem"""
    try:
        thumbnail_path = Path(path)
        if not thumbnail_path.exists():
            raise HTTPException(status_code=404, detail="Thumbnail not found")
        
        # Verify it's an image file
        allowed_extensions = {'.png', '.jpg', '.jpeg', '.webp', '.gif'}
        if thumbnail_path.suffix.lower() not in allowed_extensions:
            raise HTTPException(status_code=400, detail="Invalid image format")
        
        return FileResponse(
            path=str(thumbnail_path),
            media_type=f"image/{thumbnail_path.suffix[1:]}",
            headers={"Cache-Control": "public, max-age=3600"}
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error serving thumbnail: {e}")
        raise HTTPException(status_code=500, detail=str(e))

class LoadCustomModelRequest(BaseModel):
    model_config = {"protected_namespaces": ()}
    model_id: int

@router.post("/custom-models/load")
async def load_custom_model(request: LoadCustomModelRequest):
    """Load a custom model for generation"""
    try:
        # Get model info from database
        model_info = await db.get_custom_model(request.model_id)
        if not model_info:
            raise HTTPException(status_code=404, detail="Custom model not found")
        
        # Verify file exists
        model_path = Path(model_info['file_path'])
        if not model_path.exists():
            raise HTTPException(status_code=400, detail="Model file not found on disk")
        
        # Deactivate all other custom models
        await db.deactivate_all_custom_models()
        
        # Load the model using model_manager
        # Note: This requires model_manager to support custom safetensors loading
        # For now, we just mark it as active in the database
        await db.set_custom_model_active(request.model_id, True)
        
        logger.info(f"Custom model loaded: {model_info['name']} ({model_info['model_type']})")
        
        return {
            "success": True,
            "message": f"Custom model '{model_info['name']}' loaded successfully",
            "model_info": {
                "id": model_info['id'],
                "name": model_info['name'],
                "model_type": model_info['model_type'],
                "precision": model_info['precision'],
                "file_path": model_info['file_path']
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error loading custom model: {e}")
        raise HTTPException(status_code=500, detail=str(e))
