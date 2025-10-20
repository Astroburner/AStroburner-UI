import torch
from diffusers import (
    StableDiffusionPipeline,
    StableDiffusionXLPipeline,
    DiffusionPipeline,
    AutoPipelineForText2Image
)
from typing import Optional, Dict, Any
import logging
from pathlib import Path
from .gpu_monitor import gpu_monitor
from config import settings

logger = logging.getLogger(__name__)

class ModelManager:
    """Manage AI models with lazy loading and VRAM optimization"""
    
    AVAILABLE_MODELS = {
        "sd15": {
            "name": "Stable Diffusion 1.5",
            "model_id": "runwayml/stable-diffusion-v1-5",
            "pipeline_class": StableDiffusionPipeline,
            "type": "text2img"
        },
        "sdxl": {
            "name": "Stable Diffusion XL",
            "model_id": "stabilityai/stable-diffusion-xl-base-1.0",
            "pipeline_class": StableDiffusionXLPipeline,
            "type": "text2img"
        },
        "sdxl-turbo": {
            "name": "SDXL Turbo",
            "model_id": "stabilityai/sdxl-turbo",
            "pipeline_class": AutoPipelineForText2Image,
            "type": "text2img"
        }
    }
    
    def __init__(self):
        self.current_model: Optional[str] = None
        self.pipeline: Optional[Any] = None
        self.device = gpu_monitor.get_optimal_device()
        self.dtype = torch.float16 if self.device == "cuda" else torch.float32
        
    def load_model(self, model_key: str) -> Dict:
        """Load a model with optimization"""
        try:
            if model_key not in self.AVAILABLE_MODELS:
                return {"success": False, "error": f"Model {model_key} not found"}
            
            model_info = self.AVAILABLE_MODELS[model_key]
            
            # Unload current model if exists
            if self.pipeline is not None:
                logger.info(f"Unloading current model: {self.current_model}")
                del self.pipeline
                gpu_monitor.clear_cache()
            
            logger.info(f"Loading model: {model_info['name']}")
            
            # Load pipeline
            pipeline_class = model_info["pipeline_class"]
            
            # Configure NSFW filter based on settings
            pipeline_kwargs = {
                "torch_dtype": self.dtype,
                "use_safetensors": True,
                "cache_dir": settings.MODELS_DIR
            }
            
            # Disable NSFW filter if configured
            if settings.DISABLE_NSFW_FILTER:
                pipeline_kwargs["safety_checker"] = None
                pipeline_kwargs["requires_safety_checker"] = False
                logger.info("NSFW filter disabled (safety_checker=None)")
            else:
                logger.info("NSFW filter enabled")
            
            self.pipeline = pipeline_class.from_pretrained(
                model_info["model_id"],
                **pipeline_kwargs
            )
            
            # Move to device
            self.pipeline = self.pipeline.to(self.device)
            
            # Apply optimizations
            if self.device == "cuda":
                if settings.ENABLE_XFORMERS:
                    try:
                        self.pipeline.enable_xformers_memory_efficient_attention()
                        logger.info("xFormers enabled")
                    except Exception as e:
                        logger.warning(f"Could not enable xFormers: {e}")
                
                if settings.ENABLE_ATTENTION_SLICING:
                    self.pipeline.enable_attention_slicing(1)
                    logger.info("Attention slicing enabled")
                
                if settings.VAE_SLICING:
                    self.pipeline.enable_vae_slicing()
                    logger.info("VAE slicing enabled")
            
            self.current_model = model_key
            
            return {
                "success": True,
                "model": model_key,
                "name": model_info["name"],
                "device": self.device,
                "dtype": str(self.dtype)
            }
            
        except Exception as e:
            logger.error(f"Error loading model {model_key}: {e}")
            return {"success": False, "error": str(e)}
    
    def generate_image(
        self,
        prompt: str,
        negative_prompt: str = "",
        width: int = 512,
        height: int = 512,
        num_inference_steps: int = 30,
        guidance_scale: float = 7.5,
        num_images: int = 1,
        seed: Optional[int] = None
    ) -> Dict:
        """Generate images"""
        try:
            if self.pipeline is None:
                return {"success": False, "error": "No model loaded"}
            
            # Set seed for reproducibility
            generator = None
            if seed is not None:
                generator = torch.Generator(device=self.device).manual_seed(seed)
            
            logger.info(f"Generating image with prompt: {prompt[:50]}...")
            
            # Generate
            output = self.pipeline(
                prompt=prompt,
                negative_prompt=negative_prompt if negative_prompt else None,
                width=width,
                height=height,
                num_inference_steps=num_inference_steps,
                guidance_scale=guidance_scale,
                num_images_per_prompt=num_images,
                generator=generator
            )
            
            return {
                "success": True,
                "images": output.images,
                "num_images": len(output.images)
            }
            
        except Exception as e:
            logger.error(f"Error generating image: {e}")
            return {"success": False, "error": str(e)}
    
    def get_current_model_info(self) -> Dict:
        """Get info about currently loaded model"""
        if self.current_model is None:
            return {"loaded": False}
        
        model_info = self.AVAILABLE_MODELS[self.current_model]
        return {
            "loaded": True,
            "key": self.current_model,
            "name": model_info["name"],
            "model_id": model_info["model_id"],
            "type": model_info["type"],
            "device": self.device
        }
    
    def list_available_models(self) -> Dict:
        """List all available models"""
        return {
            "models": [
                {
                    "key": key,
                    "name": info["name"],
                    "type": info["type"],
                    "loaded": key == self.current_model
                }
                for key, info in self.AVAILABLE_MODELS.items()
            ]
        }

# Global instance
model_manager = ModelManager()
