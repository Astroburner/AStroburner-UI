"""
Model Detector Utility for Custom Models
Detects model type and precision from safetensors files
"""
import logging
from pathlib import Path
from typing import Tuple, Optional, Dict
import safetensors.torch

logger = logging.getLogger(__name__)

def get_supported_model_types() -> list:
    """Get list of supported model types"""
    return [
        "SD1.5",
        "SDXL",
        "SDXL-Turbo",
        "FLUX",
        "FLUX.1 Dev",
        "FLUX.1 Kontext",
        "Pony Diffusion XL",
        "Illustrious XL",
        "Wan 2.1 T2V",
        "Wan 2.1 I2V",
        "Wan 2.2 T2V",
        "Wan 2.2 I2V",
        "Qwen-Image",
        "Unknown"
    ]

def get_supported_precisions() -> list:
    """Get list of supported precisions"""
    return ["FP32", "FP16", "BF16", "FP8", "Unknown"]

def detect_model_type(file_path: str) -> Tuple[str, str]:
    """
    Detect model type and precision from safetensors file
    
    Args:
        file_path: Path to .safetensors file
        
    Returns:
        Tuple of (model_type, precision)
    """
    try:
        with safetensors.torch.safe_open(file_path, framework="pt") as f:
            metadata = f.metadata()
            keys = f.keys()
            
            # Detect precision from first tensor
            precision = "Unknown"
            if keys:
                first_key = list(keys)[0]
                tensor = f.get_tensor(first_key)
                tensor_dtype = str(tensor.dtype)
                
                # Map PyTorch dtypes to precision strings
                dtype_map = {
                    "torch.float32": "FP32",
                    "torch.float16": "FP16",
                    "torch.bfloat16": "BF16",
                    "torch.float8_e4m3fn": "FP8",
                    "torch.float8_e5m2": "FP8"
                }
                precision = dtype_map.get(tensor_dtype, tensor_dtype)
            
            # Detect model type from keys and metadata
            model_type = detect_model_from_keys(keys, metadata)
            
            logger.info(f"Detected model: {model_type} ({precision})")
            return (model_type, precision)
            
    except Exception as e:
        logger.error(f"Error detecting model type: {e}")
        return ("Unknown", "Unknown")

def detect_model_from_keys(keys: list, metadata: Optional[Dict] = None) -> str:
    """
    Detect model type from tensor keys and metadata
    
    Args:
        keys: List of tensor keys in safetensors file
        metadata: Optional metadata dictionary
        
    Returns:
        Detected model type string
    """
    keys_str = " ".join(keys)
    
    # Check for FLUX (Flux Transformer architecture)
    if any(k in keys_str for k in ['double_blocks', 'single_blocks', 'img_in', 'txt_in']):
        # Check for specific FLUX variants
        if 'kontext' in keys_str.lower():
            return "FLUX.1 Kontext"
        return "FLUX"
    
    # Check for SDXL variants first (more specific)
    if any(k in keys_str for k in ['conditioner.embedders', 'label_emb', 'add_embedding']):
        # Check for Pony Diffusion XL
        if metadata and 'pony' in str(metadata).lower():
            return "Pony Diffusion XL"
        # Check for Illustrious XL
        if metadata and 'illustrious' in str(metadata).lower():
            return "Illustrious XL"
        # Check for SDXL-Turbo
        if metadata and 'turbo' in str(metadata).lower():
            return "SDXL-Turbo"
        return "SDXL"
    
    # Check for SD1.5 vs SDXL by input blocks count
    if 'model.diffusion_model.input_blocks' in keys_str:
        # SDXL has 12 input blocks (0-11), SD1.5 has 9 input blocks (0-8)
        if 'model.diffusion_model.input_blocks.11' in keys_str:
            return "SDXL"
        else:
            return "SD1.5"
    
    # Check for Wan models (video generation)
    if any(k in keys_str for k in ['temporal', 'video', 'frame']):
        if 'i2v' in keys_str.lower():
            return "Wan 2.2 I2V" if '2.2' in str(metadata) else "Wan 2.1 I2V"
        if 't2v' in keys_str.lower():
            return "Wan 2.2 T2V" if '2.2' in str(metadata) else "Wan 2.1 T2V"
    
    # Check for Qwen models (text rendering)
    if any(k in keys_str for k in ['qwen', 'text_encoder']):
        return "Qwen-Image"
    
    # Default to Unknown if no pattern matches
    logger.warning(f"Could not determine model type from keys. Using 'Unknown'")
    return "Unknown"
