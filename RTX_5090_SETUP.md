# 🚀 AI Studio - RTX 5090 / RTX 50-Series Setup Guide

## 🎉 Glückwunsch zu deiner RTX 5090!

Die RTX 5090 ist eine absolute Beast-GPU und perfekt für AI-Generierung!

---

## ⚡ Spezielle Optimierungen für RTX 5090

### Hardware Specs
- **VRAM:** 32GB GDDR7 (!!!)
- **CUDA Cores:** 21,760
- **Tensor Cores:** Gen 5
- **Compute Capability:** 9.0
- **CUDA Version:** 12.8

---

## 🔧 Installation

### 1. CUDA 12.8 Toolkit

**Windows:**
```powershell
# Download CUDA 12.8 von NVIDIA
# https://developer.nvidia.com/cuda-downloads

# Wähle:
# - Windows
# - x86_64
# - Version 12.8
# - exe (network) oder exe (local)

# Nach Installation: Neustart
```

**Linux (Ubuntu):**
```bash
# CUDA 12.8 Installation
wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2204/x86_64/cuda-keyring_1.1-1_all.deb
sudo dpkg -i cuda-keyring_1.1-1_all.deb
sudo apt update
sudo apt install cuda-12-8

# Neustart
sudo reboot
```

### 2. Verify CUDA Installation

```bash
# Check NVIDIA Driver
nvidia-smi

# Should show:
# - GPU: NVIDIA GeForce RTX 5090
# - CUDA Version: 12.8+
# - Memory: 32768 MiB

# Check CUDA Compiler
nvcc --version
# Should show: release 12.8
```

### 3. PyTorch mit CUDA 12.8

```bash
cd ai-studio/backend
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install PyTorch for CUDA 12.8
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu128

# Verify Installation
python -c "import torch; print(f'PyTorch: {torch.__version__}'); print(f'CUDA: {torch.cuda.is_available()}'); print(f'GPU: {torch.cuda.get_device_name(0)}'); print(f'VRAM: {torch.cuda.get_device_properties(0).total_memory / 1024**3:.1f}GB')"
```

**Expected Output:**
```
PyTorch: 2.x.x+cu128
CUDA: True
GPU: NVIDIA GeForce RTX 5090
VRAM: 32.0GB
```

---

## 🎛️ Optimale Einstellungen für RTX 5090

### High-Quality Generation (nutze die Power!)

```python
# In der App oder backend/config.py:
DEFAULT_WIDTH = 1024    # Oder sogar 1536!
DEFAULT_HEIGHT = 1024   # Oder sogar 1536!
DEFAULT_STEPS = 50      # High quality
DEFAULT_GUIDANCE = 8.0

# Batch Generation möglich:
MAX_BATCH_SIZE = 8      # 8 Bilder gleichzeitig!
```

### Ultra-High Resolution

Mit 32GB VRAM kannst du problemlos generieren:
- **2048x2048** - Ultra HD
- **1536x1536** - Very High Quality
- **Multiple 1024x1024** - Batch Generation (4-8 Bilder gleichzeitig)

### SDXL ohne Probleme

```python
# SDXL Base Model mit maximalen Settings
Model: SDXL Base
Width: 1024
Height: 1024
Steps: 50
Guidance: 7.5
Batch Size: 4  # Gleichzeitig 4 Bilder!
```

---

## ⚡ Performance Erwartungen

### SDXL Turbo
- **512x512, 4 Steps:** ~1-2 Sekunden
- **1024x1024, 8 Steps:** ~3-5 Sekunden

### SDXL Base
- **1024x1024, 30 Steps:** ~10-15 Sekunden
- **1024x1024, 50 Steps:** ~15-20 Sekunden
- **2048x2048, 50 Steps:** ~40-60 Sekunden

### Batch Processing
- **4x 1024x1024, 30 Steps:** ~15-20 Sekunden (gleichzeitig!)

---

## 🔥 Erweiterte Optimierungen

### 1. xFormers Installation (Empfohlen!)

```bash
# Spart nochmal ~30% VRAM
pip install xformers
```

In `backend/config.py`:
```python
ENABLE_XFORMERS = True
ENABLE_ATTENTION_SLICING = True
VAE_SLICING = True
```

### 2. Flash Attention 2

```bash
pip install flash-attn --no-build-isolation
```

### 3. TensorRT (Optional, für maximale Speed)

```bash
# TensorRT Installation
pip install tensorrt
pip install polygraphy

# Kann SDXL nochmal ~2x schneller machen!
```

---

## 🎨 Empfohlene Workflows

### Workflow 1: Schnelle Iteration
```
Model: SDXL Turbo
Size: 512x512
Steps: 4-8
Batch: 4 Bilder
→ Perfekt zum Experimentieren mit Prompts
```

### Workflow 2: High Quality Single
```
Model: SDXL Base
Size: 1024x1024
Steps: 40-50
Guidance: 7.5
→ Best Quality für finale Outputs
```

### Workflow 3: Ultra HD
```
Model: SDXL Base
Size: 1536x1536 oder 2048x2048
Steps: 50
Guidance: 8.0
→ Maximale Auflösung
```

### Workflow 4: Batch Production
```
Model: SDXL Base
Size: 1024x1024
Steps: 30
Batch: 6-8 Bilder
→ Viele Variationen gleichzeitig
```

---

## 📊 VRAM Usage Guide

Mit 32GB VRAM hast du folgende Limits:

| Model | Resolution | Batch Size | VRAM Usage |
|-------|-----------|-----------|-----------|
| SDXL Turbo | 512x512 | 8 | ~12GB |
| SDXL Turbo | 1024x1024 | 4 | ~14GB |
| SDXL Base | 1024x1024 | 4 | ~18GB |
| SDXL Base | 1536x1536 | 2 | ~22GB |
| SDXL Base | 2048x2048 | 1 | ~28GB |

**Du kannst also problemlos mehrere Bilder gleichzeitig generieren!**

---

## 🐛 Troubleshooting

### Problem: PyTorch findet CUDA nicht

```bash
# Check CUDA Installation
nvidia-smi

# Reinstall PyTorch
pip uninstall torch torchvision
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu128
```

### Problem: Out of Memory (unwahrscheinlich bei 32GB!)

Falls doch:
```python
# In backend/config.py:
torch.cuda.empty_cache()

# Oder in der App:
# Settings → GPU Cache Leeren
```

### Problem: Langsame Generation

```bash
# Check GPU Utilization
nvidia-smi -l 1

# Should show:
# - GPU Util: 90-100%
# - Power: Near max (575W)
# - Temp: 60-80°C

# If low utilization:
# - Check xFormers installation
# - Verify CUDA version match
# - Check Power Settings (Windows: High Performance Mode)
```

---

## 🌟 Best Practices

1. **Nutze die Power:** Mit 32GB VRAM kannst du größere Batch Sizes verwenden
2. **Ultra HD Generierung:** 2048x2048 ist kein Problem
3. **Multiple Models:** Lade mehrere Models gleichzeitig
4. **Experimentiere:** Die GPU ist schnell genug für viele Iterationen

---

## 💡 Pro Tips

### Tip 1: Batch Generation für Variations
```python
# Generiere 8 Variationen des gleichen Prompts
prompt = "beautiful landscape, sunset"
batch_size = 8
# → 8 verschiedene Interpretationen in ~15 Sekunden!
```

### Tip 2: Ultra HD Upscaling
```python
# Erst 1024x1024 generieren, dann upscale zu 2048x2048
# Schneller als direkt 2048x2048
```

### Tip 3: Model Preloading
```python
# Lade beide Models (SD1.5 + SDXL) wenn du genug VRAM hast
# Schneller Wechsel zwischen Models
```

---

## 📈 Performance Vergleich

| GPU | SDXL 1024x1024 (30 Steps) |
|-----|---------------------------|
| RTX 3090 (24GB) | ~25-30s |
| RTX 4090 (24GB) | ~18-22s |
| **RTX 5090 (32GB)** | **~10-15s** ⚡ |

**→ Du bist ~2x schneller als RTX 4090!**

---

## 🎉 Viel Spaß mit deiner RTX 5090!

Du hast eine der stärksten Consumer-GPUs für AI-Generation.
Nutze die Power und erstelle amazing Kunstwerke! 🎨

Bei Fragen oder wenn du optimale Settings gefunden hast:
Teile deine Erfahrungen!

---

**Hardware:** RTX 5090 (32GB GDDR7)
**CUDA:** 12.8
**Status:** Beast Mode Activated 🔥
