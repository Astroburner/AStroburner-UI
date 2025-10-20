"""
Model Type Detection Utility
Automatically detect SD1.5, SDXL, FLUX, etc. from safetensors metadata
"""
import safetensors.torch
from pathlib import Path
from typing import Dict, Optional, Tuple
import logging

logger = logging.getLogger(__name__)

def detect_model_type(file_path: str) -> Tuple[str, str]:
    """
    Detect model type and precision from safetensors file
    
    Returns:
        Tuple of (model_type, precision)
        model_type: 'SD1.5', 'SDXL', 'FLUX', 'Unknown'
        precision: 'FP32', 'FP16', 'BF16', 'FP8'
    """
    try:
        path = Path(file_path)
        if not path.exists():
            return ("Unknown", "Unknown")
        
        if not path.suffix.lower() == '.safetensors':
            return ("Unknown", "Unknown")
        
        # Load metadata only (no tensors)
        with safetensors.torch.safe_open(file_path, framework="pt") as f:
            metadata = f.metadata()
            keys = f.keys()
            
            # Detect precision from first tensor
            precision = "Unknown"
            if keys:
                first_key = list(keys)[0]
                tensor_dtype = f.get_tensor(first_key).dtype
                
                # Map PyTorch dtype to precision
                dtype_map = {
                    "torch.float32": "FP32",
                    "torch.float16": "FP16",
                    "torch.bfloat16": "BF16",
                    "torch.float8_e4m3fn": "FP8",
                    "torch.float8_e5m2": "FP8"
                }
                precision = dtype_map.get(str(tensor_dtype), str(tensor_dtype))
            
            # Detect model type from keys and metadata
            model_type = detect_model_from_keys(keys, metadata)
            
            return (model_type, precision)
            
    except Exception as e:
        logger.error(f"Error detecting model type: {e}")
        return ("Unknown", "Unknown")

def detect_model_from_keys(keys: list, metadata: Optional[Dict] = None) -> str:
    """
    Detect model type from tensor keys and metadata
    
    Detection logic:
    - SD1.5: Has 'model.diffusion_model.input_blocks' and smaller U-Net
    - SDXL: Has 'conditioner.embedders' or larger U-Net with dual text encoders
    - FLUX: Has 'double_blocks' or 'single_blocks' (Flux Transformer)
    - Pony/Illustrious: Same as SDXL (SDXL-based)
    """
    keys_str = " ".join(keys)
    
    # Check for FLUX (Flux Transformer architecture)
    if any(k in keys_str for k in ['double_blocks', 'single_blocks', 'img_in', 'txt_in']):
        return "FLUX"
    
    # Check for SDXL
    if any(k in keys_str for k in [
        'conditioner.embedders',  # SDXL conditioning
        'label_emb',  # SDXL label embedding
        'add_embedding'  # SDXL additional embeddings
    ]):
        return "SDXL"
    
    # Check for SD1.5
    if 'model.diffusion_model.input_blocks' in keys_str:
        # Further differentiate by checking U-Net size
        # SDXL has more layers and larger dimensions
        if 'model.diffusion_model.input_blocks.11' in keys_str:
            return "SDXL"  # SDXL has 12 input blocks (0-11)
        else:
            return "SD1.5"  # SD1.5 has 9 input blocks
    
    # Check metadata for model type hints
    if metadata:
        meta_str = str(metadata).lower()
        if 'sdxl' in meta_str or 'xl' in meta_str:
            return "SDXL"
        if 'flux' in meta_str:
            return "FLUX"
        if 'sd1.5' in meta_str or 'sd-v1' in meta_str:
            return "SD1.5"
    
    return "Unknown"

def get_supported_model_types() -> list:
    """Get list of supported model types for user selection"""
    return [
        "SD1.5",
        "SDXL",
        "SDXL-Turbo",
        "Pony",
        "Illustrious",
        "FLUX-Dev",
        "FLUX-Kontext",
        "Wan2.1-T2V",
        "Wan2.1-I2V",
        "Wan2.2-T2V",
        "Wan2.2-I2V",
        "Wan2.2-S2V",
        "Qwen",
        "Qwen-Image-Edit"
    ]

def get_supported_precisions() -> list:
    """Get list of supported precisions"""
    return ["FP32", "FP16", "BF16", "FP8"]
