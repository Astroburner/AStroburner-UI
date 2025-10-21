import torch
from diffusers import (
    StableDiffusionPipeline,
    StableDiffusionXLPipeline,
    StableDiffusionImg2ImgPipeline,
    StableDiffusionXLImg2ImgPipeline,
    DiffusionPipeline,
    AutoPipelineForText2Image,
    AutoPipelineForImage2Image,
    DDIMScheduler,
    DDPMScheduler,
    PNDMScheduler,
    LMSDiscreteScheduler,
    EulerDiscreteScheduler,
    EulerAncestralDiscreteScheduler,
    DPMSolverMultistepScheduler,
    DPMSolverSinglestepScheduler,
    HeunDiscreteScheduler,
    KDPM2DiscreteScheduler,
    KDPM2AncestralDiscreteScheduler,
    UniPCMultistepScheduler
)
from typing import Optional, Dict, Any
import logging
from pathlib import Path
from PIL import Image
import base64
from io import BytesIO
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
            "img2img_class": StableDiffusionImg2ImgPipeline,
            "type": "text2img"
        },
        "sdxl": {
            "name": "Stable Diffusion XL",
            "model_id": "stabilityai/stable-diffusion-xl-base-1.0",
            "pipeline_class": StableDiffusionXLPipeline,
            "img2img_class": StableDiffusionXLImg2ImgPipeline,
            "type": "text2img"
        },
        "sdxl-turbo": {
            "name": "SDXL Turbo",
            "model_id": "stabilityai/sdxl-turbo",
            "pipeline_class": AutoPipelineForText2Image,
            "img2img_class": AutoPipelineForImage2Image,
            "type": "text2img"
        },
        "pony": {
            "name": "Pony Diffusion XL V6",
            "model_id": "LyliaEngine/Pony_Diffusion_V6_XL",
            "pipeline_class": StableDiffusionXLPipeline,
            "img2img_class": StableDiffusionXLImg2ImgPipeline,
            "type": "text2img"
        },
        "illustrious": {
            "name": "Illustrious XL",
            "model_id": "OnomaAIResearch/Illustrious-xl-early-release-v0",
            "pipeline_class": StableDiffusionXLPipeline,
            "img2img_class": StableDiffusionXLImg2ImgPipeline,
            "type": "text2img"
        },
        "flux-dev": {
            "name": "FLUX.1 Dev",
            "model_id": "black-forest-labs/FLUX.1-dev",
            "pipeline_class": DiffusionPipeline,
            "img2img_class": None,
            "type": "text2img"
        },
        "flux-kontext": {
            "name": "FLUX.1 Kontext Dev",
            "model_id": "black-forest-labs/FLUX.1-Kontext-dev",
            "pipeline_class": DiffusionPipeline,
            "img2img_class": None,
            "type": "image2image"
        },
        "wan21-t2v": {
            "name": "Wan 2.1 T2V 14B",
            "model_id": "Wan-AI/Wan2.1-T2V-14B",
            "pipeline_class": DiffusionPipeline,
            "img2img_class": None,
            "type": "text2video"
        },
        "wan21-i2v": {
            "name": "Wan 2.1 I2V 14B",
            "model_id": "Wan-AI/Wan2.1-I2V-14B",
            "pipeline_class": DiffusionPipeline,
            "img2img_class": None,
            "type": "image2video"
        },
        "wan22-t2v": {
            "name": "Wan 2.2 T2V 14B",
            "model_id": "Wan-AI/Wan2.2-T2V-14B",
            "pipeline_class": DiffusionPipeline,
            "img2img_class": None,
            "type": "text2video"
        },
        "wan22-i2v": {
            "name": "Wan 2.2 I2V 14B",
            "model_id": "Wan-AI/Wan2.2-I2V-14B",
            "pipeline_class": DiffusionPipeline,
            "img2img_class": None,
            "type": "image2video"
        },
        "wan22-s2v": {
            "name": "Wan 2.2 S2V 14B",
            "model_id": "Wan-AI/Wan2.2-S2V-14B",
            "pipeline_class": DiffusionPipeline,
            "img2img_class": None,
            "type": "speech2video"
        },
        "qwen": {
            "name": "Qwen-Image",
            "model_id": "Qwen/Qwen-Image",
            "pipeline_class": DiffusionPipeline,
            "img2img_class": None,
            "type": "text2img"
        },
        "qwen-image-edit": {
            "name": "Qwen-Image Edit",
            "model_id": "Qwen/Qwen-Image",
            "pipeline_class": DiffusionPipeline,
            "img2img_class": None,
            "type": "image2image"
        }
    }
    
    SCHEDULER_MAP = {
        "DDIM": DDIMScheduler,
        "DDPM": DDPMScheduler,
        "PNDM": PNDMScheduler,
        "LMSDiscrete": LMSDiscreteScheduler,
        "EulerDiscrete": EulerDiscreteScheduler,
        "EulerAncestralDiscrete": EulerAncestralDiscreteScheduler,
        "DPMSolverMultistep": DPMSolverMultistepScheduler,
        "DPMSolverSinglestep": DPMSolverSinglestepScheduler,
        "HeunDiscrete": HeunDiscreteScheduler,
        "KDPM2Discrete": KDPM2DiscreteScheduler,
        "KDPM2AncestralDiscrete": KDPM2AncestralDiscreteScheduler,
        "UniPCMultistep": UniPCMultistepScheduler
    }
    
    def __init__(self):
        self.current_model: Optional[str] = None
        self.pipeline: Optional[Any] = None
        self.img2img_pipeline: Optional[Any] = None
        self.device = gpu_monitor.get_optimal_device()
        self.dtype = torch.float16 if self.device == "cuda" else torch.float32
        self.loaded_loras: list = []  # Track loaded LoRAs
        
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
                if self.img2img_pipeline is not None:
                    del self.img2img_pipeline
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
            
            # Also load img2img pipeline
            img2img_class = model_info.get("img2img_class")
            if img2img_class:
                logger.info("Loading img2img pipeline...")
                self.img2img_pipeline = img2img_class.from_pretrained(
                    model_info["model_id"],
                    **pipeline_kwargs
                )
                self.img2img_pipeline = self.img2img_pipeline.to(self.device)
                
                # Apply same optimizations
                if self.device == "cuda":
                    if settings.ENABLE_XFORMERS:
                        try:
                            self.img2img_pipeline.enable_xformers_memory_efficient_attention()
                        except Exception as e:
                            logger.warning(f"Could not enable xFormers for img2img: {e}")
                    if settings.ENABLE_ATTENTION_SLICING:
                        self.img2img_pipeline.enable_attention_slicing(1)
                    if settings.VAE_SLICING:
                        self.img2img_pipeline.enable_vae_slicing()
            
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
    
    def load_custom_model(self, model_path: str, model_type: str, model_name: str) -> Dict:
        """Load a custom .safetensors model from local filesystem"""
        try:
            # Unload current model if exists
            if self.pipeline is not None:
                logger.info(f"Unloading current model: {self.current_model}")
                del self.pipeline
                if self.img2img_pipeline is not None:
                    del self.img2img_pipeline
                gpu_monitor.clear_cache()
            
            logger.info(f"Loading custom model: {model_name} ({model_type}) from {model_path}")
            
            # Determine pipeline class based on model type
            pipeline_class = None
            img2img_class = None
            
            if model_type in ["SD1.5"]:
                pipeline_class = StableDiffusionPipeline
                img2img_class = StableDiffusionImg2ImgPipeline
            elif model_type in ["SDXL", "SDXL-Turbo", "Pony Diffusion XL", "Illustrious XL"]:
                pipeline_class = StableDiffusionXLPipeline
                img2img_class = StableDiffusionXLImg2ImgPipeline
            elif model_type in ["FLUX", "FLUX.1 Dev", "FLUX.1 Kontext"]:
                pipeline_class = DiffusionPipeline
                img2img_class = None
            else:
                # Default to SDXL for unknown types
                logger.warning(f"Unknown model type {model_type}, defaulting to SDXL pipeline")
                pipeline_class = StableDiffusionXLPipeline
                img2img_class = StableDiffusionXLImg2ImgPipeline
            
            # Configure pipeline
            pipeline_kwargs = {
                "torch_dtype": self.dtype,
                "use_safetensors": True,
            }
            
            # Disable NSFW filter if configured
            if settings.DISABLE_NSFW_FILTER:
                pipeline_kwargs["safety_checker"] = None
                pipeline_kwargs["requires_safety_checker"] = False
                logger.info("NSFW filter disabled for custom model")
            
            # Load from single file
            self.pipeline = pipeline_class.from_single_file(
                model_path,
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
            
            # Load img2img pipeline if supported
            if img2img_class:
                logger.info("Loading img2img pipeline for custom model...")
                self.img2img_pipeline = img2img_class.from_single_file(
                    model_path,
                    **pipeline_kwargs
                )
                self.img2img_pipeline = self.img2img_pipeline.to(self.device)
                
                # Apply optimizations
                if self.device == "cuda":
                    if settings.ENABLE_XFORMERS:
                        try:
                            self.img2img_pipeline.enable_xformers_memory_efficient_attention()
                        except Exception as e:
                            logger.warning(f"Could not enable xFormers for img2img: {e}")
                    if settings.ENABLE_ATTENTION_SLICING:
                        self.img2img_pipeline.enable_attention_slicing(1)
                    if settings.VAE_SLICING:
                        self.img2img_pipeline.enable_vae_slicing()
            
            self.current_model = f"custom:{model_name}"
            
            return {
                "success": True,
                "model": f"custom:{model_name}",
                "name": model_name,
                "type": model_type,
                "path": model_path,
                "device": self.device,
                "dtype": str(self.dtype)
            }
            
        except Exception as e:
            logger.error(f"Error loading custom model {model_name}: {e}")
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
        seed: Optional[int] = None,
        scheduler: Optional[str] = None
    ) -> Dict:
        """Generate images"""
        try:
            if self.pipeline is None:
                return {"success": False, "error": "No model loaded"}
            
            # Set scheduler if specified
            self._set_scheduler(self.pipeline, scheduler)
            
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
    
    def _set_scheduler(self, pipeline: Any, scheduler_name: Optional[str]) -> None:
        """Set scheduler for pipeline"""
        if scheduler_name and scheduler_name in self.SCHEDULER_MAP:
            try:
                scheduler_class = self.SCHEDULER_MAP[scheduler_name]
                pipeline.scheduler = scheduler_class.from_config(pipeline.scheduler.config)
                logger.info(f"Scheduler set to: {scheduler_name}")
            except Exception as e:
                logger.warning(f"Could not set scheduler {scheduler_name}: {e}")

    def generate_img2img(
        self,
        prompt: str,
        input_image_base64: str,
        negative_prompt: str = "",
        width: int = 512,
        height: int = 512,
        num_inference_steps: int = 30,
        guidance_scale: float = 7.5,
        num_images: int = 1,
        seed: Optional[int] = None,
        scheduler: Optional[str] = None,
        strength: float = 0.75
    ) -> Dict:
        """Generate images from input image (img2img)"""
        try:
            if self.img2img_pipeline is None:
                return {"success": False, "error": "No img2img model loaded"}
            
            # Decode base64 image
            try:
                if "," in input_image_base64:
                    input_image_base64 = input_image_base64.split(",")[1]
                
                image_data = base64.b64decode(input_image_base64)
                input_image = Image.open(BytesIO(image_data)).convert("RGB")
                input_image = input_image.resize((width, height), Image.LANCZOS)
                logger.info(f"Input image loaded and resized to {width}x{height}")
            except Exception as e:
                logger.error(f"Error decoding input image: {e}")
                return {"success": False, "error": f"Invalid input image: {str(e)}"}
            
            self._set_scheduler(self.img2img_pipeline, scheduler)
            
            generator = None
            if seed is not None:
                generator = torch.Generator(device=self.device).manual_seed(seed)
            
            logger.info(f"Generating img2img with strength={strength}, prompt: {prompt[:50]}...")
            
            output = self.img2img_pipeline(
                prompt=prompt,
                image=input_image,
                negative_prompt=negative_prompt if negative_prompt else None,
                num_inference_steps=num_inference_steps,
                guidance_scale=guidance_scale,
                num_images_per_prompt=num_images,
                generator=generator,
                strength=strength
            )
            
            return {
                "success": True,
                "images": output.images,
                "num_images": len(output.images)
            }
            
        except Exception as e:
            logger.error(f"Error generating img2img: {e}")
            return {"success": False, "error": str(e)}
    
    def get_current_model_info(self) -> Dict:
        """Get info about currently loaded model"""
        if self.current_model is None:
            return {"loaded": False}
        
        # Check if it's a custom model
        if self.current_model.startswith("custom:"):
            model_name = self.current_model[7:]  # Remove "custom:" prefix
            return {
                "loaded": True,
                "key": self.current_model,
                "name": model_name,
                "model_id": "custom",
                "type": "custom",
                "device": self.device
            }
        
        # Regular model from AVAILABLE_MODELS
        if self.current_model not in self.AVAILABLE_MODELS:
            return {"loaded": False, "error": "Unknown model"}
        
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
        from huggingface_hub import scan_cache_dir
        
        # Scan HuggingFace cache to check which models are downloaded
        downloaded_models = set()
        try:
            cache_info = scan_cache_dir()
            for repo in cache_info.repos:
                # Extract repo ID from repo_id attribute
                repo_id = repo.repo_id
                downloaded_models.add(repo_id)
        except Exception as e:
            logger.warning(f"Could not scan HuggingFace cache: {e}")
        
        return {
            "models": [
                {
                    "key": key,
                    "name": info["name"],
                    "type": info["type"],
                    "loaded": key == self.current_model,
                    "downloaded": info["model_id"] in downloaded_models
                }
                for key, info in self.AVAILABLE_MODELS.items()
            ]
        }
    
    def load_loras(self, loras: list) -> Dict:
        """Load multiple LoRAs (up to 5) into the pipeline using modern diffusers API"""
        try:
            if self.pipeline is None:
                return {"success": False, "error": "No model loaded"}
            
            if len(loras) > 5:
                return {"success": False, "error": "Maximum 5 LoRAs can be loaded at once"}
            
            # Unload existing LoRAs first
            self.unload_all_loras()
            
            # Prepare adapter names and weights
            adapter_names = []
            adapter_weights = []
            
            # Load each LoRA
            for lora in loras:
                file_path = lora.get("file_path")
                weight = lora.get("weight", 1.0)
                lora_name = lora.get("name", "lora")
                
                if not Path(file_path).exists():
                    logger.warning(f"LoRA file not found: {file_path}")
                    continue
                
                try:
                    # Load LoRA weights using modern diffusers API (no PEFT required)
                    logger.info(f"Loading LoRA: {lora_name} from {file_path} with weight {weight}")
                    
                    # Load LoRA into pipeline using directory-based loading
                    # This works without PEFT backend
                    lora_dir = str(Path(file_path).parent)
                    lora_file = Path(file_path).name
                    
                    self.pipeline.load_lora_weights(
                        lora_dir,
                        weight_name=lora_file,
                        adapter_name=lora_name
                    )
                    
                    adapter_names.append(lora_name)
                    adapter_weights.append(weight)
                    
                    # Same for img2img pipeline if exists
                    if self.img2img_pipeline:
                        self.img2img_pipeline.load_lora_weights(
                            lora_dir,
                            weight_name=lora_file,
                            adapter_name=lora_name
                        )
                    
                    self.loaded_loras.append(lora)
                    logger.info(f"LoRA loaded successfully: {lora_name}")
                    
                except Exception as e:
                    logger.error(f"Error loading LoRA {lora_name}: {e}")
                    continue
            
            # Set all adapters with their weights if any were loaded
            if adapter_names:
                try:
                    self.pipeline.set_adapters(adapter_names, adapter_weights=adapter_weights)
                    if self.img2img_pipeline:
                        self.img2img_pipeline.set_adapters(adapter_names, adapter_weights=adapter_weights)
                    logger.info(f"Set {len(adapter_names)} adapter(s) with weights: {adapter_weights}")
                except Exception as e:
                    logger.warning(f"Could not set adapters (PEFT may not be available): {e}")
                    # Fallback: Use fuse_lora for non-PEFT systems
                    try:
                        for name, weight in zip(adapter_names, adapter_weights):
                            self.pipeline.fuse_lora(lora_scale=weight)
                            if self.img2img_pipeline:
                                self.img2img_pipeline.fuse_lora(lora_scale=weight)
                        logger.info(f"Fused LoRAs with weights (PEFT-free method)")
                    except Exception as e2:
                        logger.error(f"Fallback LoRA fusion also failed: {e2}")
            
            return {
                "success": True,
                "loaded_count": len(self.loaded_loras),
                "loras": [l.get("name") for l in self.loaded_loras]
            }
            
        except Exception as e:
            logger.error(f"Error loading LoRAs: {e}")
            return {"success": False, "error": str(e)}
    
    def unload_all_loras(self):
        """Unload all LoRAs from the pipeline (PEFT-free method)"""
        try:
            if self.pipeline and hasattr(self.pipeline, 'unload_lora_weights'):
                try:
                    self.pipeline.unload_lora_weights()
                    logger.info("Unloaded all LoRAs from txt2img pipeline")
                except Exception as e:
                    logger.warning(f"Error unloading LoRAs (PEFT may not be available): {e}")
                    # Fallback: Try unfuse_lora for non-PEFT systems
                    try:
                        if hasattr(self.pipeline, 'unfuse_lora'):
                            self.pipeline.unfuse_lora()
                            logger.info("Unfused LoRAs from txt2img pipeline (PEFT-free method)")
                    except:
                        pass
            
            if self.img2img_pipeline and hasattr(self.img2img_pipeline, 'unload_lora_weights'):
                try:
                    self.img2img_pipeline.unload_lora_weights()
                    logger.info("Unloaded all LoRAs from img2img pipeline")
                except Exception as e:
                    logger.warning(f"Error unloading LoRAs from img2img: {e}")
                    try:
                        if hasattr(self.img2img_pipeline, 'unfuse_lora'):
                            self.img2img_pipeline.unfuse_lora()
                            logger.info("Unfused LoRAs from img2img pipeline (PEFT-free method)")
                    except:
                        pass
            
            self.loaded_loras = []
            
        except Exception as e:
            logger.warning(f"Error unloading LoRAs: {e}")
    
    def get_loaded_loras(self) -> list:
        """Get list of currently loaded LoRAs"""
        return self.loaded_loras

# Global instance
model_manager = ModelManager()
