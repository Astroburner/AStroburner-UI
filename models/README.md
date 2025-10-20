# AI Studio - Models Directory

This directory stores downloaded AI models for local GPU-accelerated inference.

## 📁 Directory Structure

```
models/
├── __init__.py           # Python module initialization
├── README.md             # This file
├── sd15/                 # Stable Diffusion 1.5 models
├── sdxl/                 # SDXL Base models
├── sdxl-turbo/          # SDXL Turbo models
├── flux/                 # Flux.1 models (planned)
├── pony/                 # Pony Diffusion models (planned)
├── illustrious/         # Illustrious XL models (planned)
└── lora/                # LoRA weights (planned)
```

## 🎯 Supported Models

### Currently Available

| Model | Size | Resolution | Speed | Quality |
|-------|------|------------|-------|---------|
| SD1.5 | 4-7 GB | 512x512 | Fast | Good |
| SDXL Base | 12-15 GB | 1024x1024 | Medium | Excellent |
| SDXL Turbo | 12-15 GB | 1024x1024 | Very Fast | Good |

### Planned Support

- **Flux.1**: Next-gen model with superior quality (~20-25 GB)
- **Pony Diffusion**: Anime-focused model (~12-15 GB)
- **Illustrious XL**: High-quality illustration model (~12-15 GB)
- **LoRA Support**: Fine-tuned model weights

## 💾 Storage Requirements

### Minimum
- **50 GB** free disk space for basic setup (SD1.5 + SDXL)

### Recommended
- **100 GB** free disk space for all models + cache
- **SSD storage** for faster model loading

### VRAM Requirements (GPU)

| Model | Minimum VRAM | Recommended VRAM |
|-------|--------------|------------------|
| SD1.5 | 4 GB | 8 GB |
| SDXL Base | 8 GB | 16 GB |
| SDXL Turbo | 8 GB | 16 GB |
| Flux.1 | 12 GB | 24 GB |

**Note**: RTX 5090 with 32GB VRAM can run all models comfortably!

## 📥 Model Download

Models are downloaded automatically on first use from Hugging Face Hub.

### Default Model Sources

- **SD1.5**: `runwayml/stable-diffusion-v1-5`
- **SDXL Base**: `stabilityai/stable-diffusion-xl-base-1.0`
- **SDXL Turbo**: `stabilityai/sdxl-turbo`

### Custom Model Location

To use a custom models directory, set the `HF_HOME` environment variable:

**Windows:**
```cmd
set HF_HOME=D:\AI_Models
```

**Linux/Mac:**
```bash
export HF_HOME=/path/to/models
```

Add this to your environment variables to make it permanent.

## ⚙️ Configuration

The models directory is configured in `backend/config.py`:

```python
from pathlib import Path

# Project root
BASE_DIR = Path(__file__).parent.parent

# Models directory (in project root, not backend)
MODELS_DIR = BASE_DIR / "models"
```

## 🚀 Usage

Models are managed by `backend/core/model_manager.py`:

```python
from core.model_manager import ModelManager

# Initialize model manager
manager = ModelManager()

# Load model (downloads if not cached)
await manager.load_model("sdxl")

# Generate image
image = await manager.generate_image(
    prompt="A beautiful sunset over mountains",
    model_name="sdxl",
    width=1024,
    height=1024
)
```

## 🔧 Advanced Configuration

### Optimizations for RTX 5090

The ModelManager automatically applies these optimizations:

1. **xFormers Memory-Efficient Attention**
   - Reduces VRAM usage by 30-40%
   - Enables larger batch sizes

2. **Attention Slicing**
   - Processes attention in smaller chunks
   - Prevents OOM errors

3. **VAE Slicing**
   - Decodes images in tiles
   - Enables ultra-high resolution (up to 4096x4096)

4. **Lazy Loading**
   - Models loaded only when needed
   - Automatic unloading of unused models

### Performance Tips

1. **First Run**: Model download takes 5-15 minutes depending on internet speed
2. **Subsequent Runs**: Models load from cache in ~10-30 seconds
3. **Warm-up Generation**: First generation is slower due to CUDA initialization
4. **Batch Processing**: Generate multiple images at once for better efficiency

## 📊 Model Performance (RTX 5090)

### Expected Generation Times

| Model | Resolution | Steps | Time | VRAM |
|-------|------------|-------|------|------|
| SD1.5 | 512x512 | 20 | 1-2s | 3-4 GB |
| SD1.5 | 1024x1024 | 20 | 3-5s | 4-6 GB |
| SDXL Base | 1024x1024 | 20 | 4-6s | 8-10 GB |
| SDXL Base | 2048x2048 | 20 | 12-15s | 16-20 GB |
| SDXL Turbo | 1024x1024 | 4 | 1-2s | 8-10 GB |

**Note**: Times are approximate and vary based on prompt complexity.

## 🛠️ Troubleshooting

### Model Not Downloading

**Problem**: Model download fails or hangs

**Solutions**:
1. Check internet connection
2. Verify Hugging Face is accessible
3. Check disk space (need 2x model size for download + extraction)
4. Try manual download:
   ```bash
   cd backend
   venv\Scripts\activate
   python -c "from diffusers import StableDiffusionPipeline; StableDiffusionPipeline.from_pretrained('runwayml/stable-diffusion-v1-5')"
   ```

### Out of Memory (OOM)

**Problem**: CUDA out of memory error during generation

**Solutions**:
1. Reduce image resolution
2. Lower `num_inference_steps`
3. Enable CPU offloading in `model_manager.py`:
   ```python
   pipe.enable_sequential_cpu_offload()
   ```

### Slow Generation

**Problem**: Generation takes longer than expected

**Solutions**:
1. Verify CUDA is enabled: Check GPU info in frontend header
2. Update GPU drivers: Latest drivers improve performance
3. Close other GPU-intensive applications
4. Check GPU usage: `nvidia-smi` should show ~95-100% utilization

### Model Files Corrupt

**Problem**: Model fails to load with errors

**Solutions**:
1. Delete cached model:
   ```cmd
   rmdir /s /q %USERPROFILE%\.cache\huggingface\hub
   ```
2. Re-download model (automatic on next generation)

## 📚 Resources

- [Hugging Face Diffusers Documentation](https://huggingface.co/docs/diffusers)
- [Stable Diffusion Guide](https://stability.ai/stable-diffusion)
- [Model Cards on Hugging Face Hub](https://huggingface.co/models?pipeline_tag=text-to-image)

## 🔐 License Notes

- **SD1.5**: CreativeML Open RAIL-M License
- **SDXL**: CreativeML Open RAIL++-M License
- **Commercial Use**: Check individual model licenses

## 💡 Tips for Best Results

1. **Use descriptive prompts**: More details = better results
2. **Adjust CFG scale**: 7-9 for balanced results
3. **Experiment with steps**: 20-30 for quality, 4-8 for speed (Turbo)
4. **Try different seeds**: Same prompt, different results
5. **Negative prompts**: Specify what you don't want

---

**Need Help?** See `TROUBLESHOOTING.md` in the project root or open an issue on GitHub.
