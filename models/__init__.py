"""
AI Studio - Models Directory

This directory stores downloaded AI models for local inference.
Models are automatically downloaded on first use.

Supported Model Types:
- Stable Diffusion 1.5 (SD1.5)
- Stable Diffusion XL Base (SDXL)
- Stable Diffusion XL Turbo (SDXL-Turbo)
- Flux.1 (planned)
- Pony Diffusion (planned)
- Illustrious XL (planned)

Directory Structure:
models/
├── sd15/                 # Stable Diffusion 1.5 models
├── sdxl/                 # SDXL Base models
├── sdxl-turbo/          # SDXL Turbo models
├── flux/                 # Flux.1 models (planned)
├── pony/                 # Pony Diffusion models (planned)
├── illustrious/         # Illustrious XL models (planned)
└── lora/                # LoRA weights (planned)

Configuration:
The models directory path is configured in backend/config.py:
- MODELS_DIR = project_root / "models"

Usage:
Models are loaded lazily by the ModelManager in backend/core/model_manager.py
The first generation with a model will download it automatically from Hugging Face.

Storage Requirements:
- SD1.5: ~4-7 GB per model
- SDXL Base: ~12-15 GB per model
- SDXL Turbo: ~12-15 GB per model
- Flux.1: ~20-25 GB per model (planned)
- Pony: ~12-15 GB per model (planned)
- Illustrious: ~12-15 GB per model (planned)

Total: Plan for at least 50-100 GB of free disk space.

Environment Variables:
Set HF_HOME to change the Hugging Face cache directory:
  export HF_HOME=/path/to/custom/cache  # Linux/Mac
  set HF_HOME=C:\path\to\custom\cache   # Windows

For more information, see:
- backend/MODELS.md
- backend/core/model_manager.py
"""

__version__ = "1.0.0"
__all__ = []
