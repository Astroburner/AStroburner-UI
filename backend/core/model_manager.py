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
from transformers import CLIPTextModel, CLIPTextConfig
from typing import Optional, Dict, Any, Tuple
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
        
        # CLIP Skip support
        self.current_model_id: Optional[str] = None  # Store model_id for encoder reloading
        self.original_text_encoder: Optional[Any] = None  # Backup original encoder
        self.original_text_encoder_2: Optional[Any] = None  # Backup SDXL second encoder
        self.current_clip_skip: int = 0  # Track current CLIP Skip value
        self.encoder_cache: Dict[Tuple[str, int], Any] = {}  # Cache: (model_id, clip_skip) -> encoder
        
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
            self.current_model_id = model_info["model_id"]  # Store for CLIP Skip
            
            # Backup original text encoders for CLIP Skip
            if hasattr(self.pipeline, 'text_encoder'):
                self.original_text_encoder = self.pipeline.text_encoder
                logger.info("Original text_encoder backed up for CLIP Skip")
            if hasattr(self.pipeline, 'text_encoder_2'):
                self.original_text_encoder_2 = self.pipeline.text_encoder_2
                logger.info("Original text_encoder_2 backed up for CLIP Skip (SDXL)")
            
            # Reset CLIP Skip state
            self.current_clip_skip = 0
            self.encoder_cache.clear()
            
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
        scheduler: Optional[str] = None,
        clip_skip: int = 0
    ) -> Dict:
        """Generate images"""
        try:
            if self.pipeline is None:
                return {"success": False, "error": "No model loaded"}
            
            # Apply CLIP Skip by replacing text encoder if needed
            if clip_skip != self.current_clip_skip:
                logger.info(f"Applying CLIP Skip: {clip_skip}")
                self._apply_clip_skip(clip_skip)
                self.current_clip_skip = clip_skip
            
            # Set scheduler if specified
            self._set_scheduler(self.pipeline, scheduler)
            
            # Set seed for reproducibility
            generator = None
            if seed is not None:
                generator = torch.Generator(device=self.device).manual_seed(seed)
            
            logger.info(f"Generating image with prompt: {prompt[:50]}...")
            
            # Generate image with properly applied CLIP Skip
            pipeline_kwargs = {
                "prompt": prompt,
                "negative_prompt": negative_prompt if negative_prompt else None,
                "width": width,
                "height": height,
                "num_inference_steps": num_inference_steps,
                "guidance_scale": guidance_scale,
                "num_images_per_prompt": num_images,
                "generator": generator
            }
            
            output = self.pipeline(**pipeline_kwargs)
            
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
    
    def _apply_clip_skip(self, clip_skip: int) -> None:
        """
        Apply CLIP Skip by replacing text encoder with truncated version.
        
        CLIP Skip works by using fewer layers of the CLIP text encoder:
        - clip_skip=0: Use all layers (standard behavior)
        - clip_skip=1: Skip last layer (more literal interpretation)
        - clip_skip=2: Skip last 2 layers (recommended for Pony/Anime models)
        - clip_skip=3: Skip last 3 layers (maximum artistic freedom)
        
        This is done by:
        1. Loading CLIPTextModel config
        2. Reducing num_hidden_layers by (clip_skip - 1)
        3. Reloading text encoder with truncated config
        4. Replacing pipeline's text_encoder
        
        For SDXL: Both text_encoder and text_encoder_2 are replaced
        """
        try:
            if not hasattr(self.pipeline, 'text_encoder'):
                logger.warning("Pipeline has no text_encoder, CLIP Skip not supported")
                return
            
            if self.current_model_id is None:
                logger.warning("No model_id stored, cannot apply CLIP Skip")
                return
            
            # Restore original encoders if clip_skip=0
            if clip_skip == 0:
                if self.original_text_encoder is not None:
                    logger.info("Restoring original text_encoder (CLIP Skip disabled)")
                    self.pipeline.text_encoder = self.original_text_encoder
                if self.original_text_encoder_2 is not None:
                    logger.info("Restoring original text_encoder_2 (CLIP Skip disabled)")
                    self.pipeline.text_encoder_2 = self.original_text_encoder_2
                return
            
            # Check cache first to avoid redundant loading
            cache_key_1 = (self.current_model_id, clip_skip, 1)
            cache_key_2 = (self.current_model_id, clip_skip, 2)
            
            # Replace text_encoder (exists in all SD models)
            if cache_key_1 in self.encoder_cache:
                logger.info(f"Using cached text_encoder for CLIP Skip {clip_skip}")
                self.pipeline.text_encoder = self.encoder_cache[cache_key_1]
            else:
                logger.info(f"Loading new text_encoder with CLIP Skip {clip_skip}")
                new_encoder = self._load_truncated_text_encoder(
                    self.current_model_id, 
                    "text_encoder", 
                    clip_skip
                )
                if new_encoder:
                    self.pipeline.text_encoder = new_encoder
                    self.encoder_cache[cache_key_1] = new_encoder
                    logger.info(f"✓ text_encoder replaced (skipping last {clip_skip} layer(s))")
            
            # Replace text_encoder_2 for SDXL models
            if hasattr(self.pipeline, 'text_encoder_2'):
                if cache_key_2 in self.encoder_cache:
                    logger.info(f"Using cached text_encoder_2 for CLIP Skip {clip_skip}")
                    self.pipeline.text_encoder_2 = self.encoder_cache[cache_key_2]
                else:
                    logger.info(f"Loading new text_encoder_2 with CLIP Skip {clip_skip}")
                    new_encoder_2 = self._load_truncated_text_encoder(
                        self.current_model_id,
                        "text_encoder_2",
                        clip_skip
                    )
                    if new_encoder_2:
                        self.pipeline.text_encoder_2 = new_encoder_2
                        self.encoder_cache[cache_key_2] = new_encoder_2
                        logger.info(f"✓ text_encoder_2 replaced (SDXL dual-encoder)")
            
            logger.info(f"CLIP Skip {clip_skip} successfully applied!")
            
        except Exception as e:
            logger.error(f"Failed to apply CLIP Skip: {e}")
            logger.warning("Continuing with original text encoder")
    
    def _load_truncated_text_encoder(
        self, 
        model_id: str, 
        subfolder: str,
        clip_skip: int
    ) -> Optional[Any]:
        """
        Load a CLIPTextModel with truncated layers for CLIP Skip.
        
        Args:
            model_id: HuggingFace model ID (e.g., "runwayml/stable-diffusion-v1-5")
            subfolder: Subfolder name ("text_encoder" or "text_encoder_2")
            clip_skip: Number of layers to skip (1-3)
        
        Returns:
            Truncated CLIPTextModel or None if loading fails
        """
        try:
            # Load original config
            text_config = CLIPTextConfig.from_pretrained(
                model_id,
                subfolder=subfolder,
                cache_dir=settings.MODELS_DIR
            )
            
            original_layers = text_config.num_hidden_layers
            
            # Calculate new layer count
            # clip_skip=2 means we want to skip the last layer before the final output
            # So we reduce by (clip_skip - 1)
            new_layers = original_layers - (clip_skip - 1)
            
            if new_layers <= 0:
                logger.error(f"Invalid CLIP Skip {clip_skip}: would result in {new_layers} layers")
                return None
            
            logger.info(f"Truncating {subfolder}: {original_layers} → {new_layers} layers")
            
            # Create truncated config
            text_config.num_hidden_layers = new_layers
            
            # Load text encoder with truncated config
            text_encoder = CLIPTextModel.from_pretrained(
                model_id,
                subfolder=subfolder,
                config=text_config,
                torch_dtype=self.dtype,
                cache_dir=settings.MODELS_DIR
            )
            
            # Move to device
            text_encoder = text_encoder.to(self.device)
            
            return text_encoder
            
        except Exception as e:
            logger.error(f"Failed to load truncated text encoder from {subfolder}: {e}")
            return None

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
        """Load multiple LoRAs (up to 5) using PEFT-free fuse_lora method"""
        try:
            if self.pipeline is None:
                return {"success": False, "error": "No model loaded"}
            
            if len(loras) > 5:
                return {"success": False, "error": "Maximum 5 LoRAs can be loaded at once"}
            
            # Unload existing LoRAs first
            self.unload_all_loras()
            
            # Load each LoRA using fuse_lora (PEFT-free method)
            for lora in loras:
                file_path = lora.get("file_path")
                weight = lora.get("weight", 1.0)
                lora_name = lora.get("name", "lora")
                
                if not Path(file_path).exists():
                    logger.warning(f"LoRA file not found: {file_path}")
                    continue
                
                try:
                    logger.info(f"Loading LoRA (PEFT-free): {lora_name} from {file_path} with weight {weight}")
                    
                    # Use direct fuse_lora instead of load_lora_weights + set_adapters
                    # This bypasses PEFT requirement entirely
                    lora_dir = str(Path(file_path).parent)
                    lora_file = Path(file_path).name
                    
                    # Load and fuse LoRA into pipeline weights directly
                    self.pipeline.load_lora_weights(lora_dir, weight_name=lora_file)
                    self.pipeline.fuse_lora(lora_scale=weight)
                    logger.info(f"LoRA fused into txt2img pipeline: {lora_name} (scale={weight})")
                    
                    # Same for img2img pipeline if exists
                    if self.img2img_pipeline:
                        self.img2img_pipeline.load_lora_weights(lora_dir, weight_name=lora_file)
                        self.img2img_pipeline.fuse_lora(lora_scale=weight)
                        logger.info(f"LoRA fused into img2img pipeline: {lora_name} (scale={weight})")
                    
                    self.loaded_loras.append(lora)
                    logger.info(f"✓ LoRA loaded successfully: {lora_name}")
                    
                except Exception as e:
                    logger.error(f"Error loading LoRA {lora_name}: {e}")
                    # Continue with other LoRAs even if one fails
                    continue
            
            return {
                "success": True,
                "loaded_count": len(self.loaded_loras),
                "loras": [l.get("name") for l in self.loaded_loras],
                "method": "fuse_lora (PEFT-free)"
            }
            
        except Exception as e:
            logger.error(f"Error loading LoRAs: {e}")
            return {"success": False, "error": str(e)}
    
    def unload_all_loras(self):
        """Unload all LoRAs from the pipeline (PEFT-free unfuse method)"""
        try:
            # Use unfuse_lora instead of unload_lora_weights to avoid PEFT requirement
            if self.pipeline and hasattr(self.pipeline, 'unfuse_lora'):
                try:
                    self.pipeline.unfuse_lora()
                    logger.info("✓ Unfused LoRAs from txt2img pipeline (PEFT-free)")
                except Exception as e:
                    logger.warning(f"Could not unfuse LoRAs from txt2img: {e}")
            
            if self.img2img_pipeline and hasattr(self.img2img_pipeline, 'unfuse_lora'):
                try:
                    self.img2img_pipeline.unfuse_lora()
                    logger.info("✓ Unfused LoRAs from img2img pipeline (PEFT-free)")
                except Exception as e:
                    logger.warning(f"Could not unfuse LoRAs from img2img: {e}")
            
            self.loaded_loras = []
            
        except Exception as e:
            logger.warning(f"Error unloading LoRAs: {e}")
    
    def get_loaded_loras(self) -> list:
        """Get list of currently loaded LoRAs"""
        return self.loaded_loras

# Global instance
model_manager = ModelManager()
