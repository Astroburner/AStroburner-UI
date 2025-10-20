# Advanced Models Architecture - AI Studio v1.7.1

## ⚠️ WICHTIG: Spezielle Komponenten für neue Modelle

Die neuen Modelle in v1.7.1 verwenden **NICHT** die Standard Stable Diffusion Architektur!

---

## 🏗️ Architektur-Übersicht

### **Standard SD/SDXL Modelle:**
```
┌─────────────────────────────────────┐
│ Standard Stable Diffusion Pipeline  │
├─────────────────────────────────────┤
│ ✅ CLIP Text Encoder                │
│ ✅ U-Net Denoising Model            │
│ ✅ VAE (Autoencoder)                │
└─────────────────────────────────────┘

Funktioniert mit:
- SD1.5
- SDXL
- SDXL-Turbo
- Pony Diffusion XL
- Illustrious XL
```

---

### **FLUX.1 Modelle - Spezielle Architektur:**
```
┌─────────────────────────────────────┐
│ FLUX.1 Architecture (12B params)    │
├─────────────────────────────────────┤
│ ✅ CLIP-L Text Encoder              │
│ ✅ T5-XXL Text Encoder (4.7B!)      │
│ ✅ Flux Transformer (DiT)           │
│ ✅ FLUX-VAE (eigener VAE)           │
└─────────────────────────────────────┘

Komponenten:
1. Text Encoders (Dual):
   - CLIP: openai/clip-vit-large-patch14
   - T5: google/t5-v1_1-xxl (4.7B Parameter!)

2. Transformer:
   - Rectified Flow Transformer
   - 12 Milliarden Parameter
   - MMDiT-Blocks (Multi-Modal)

3. VAE:
   - black-forest-labs/FLUX.1-dev (eigener VAE)
   - Nicht kompatibel mit SD-VAE!

VRAM: 24+ GB (wegen T5-XXL!)
```

**Hugging Face Pipeline:**
```python
from diffusers import FluxPipeline

# Korrekte Verwendung:
pipe = FluxPipeline.from_pretrained(
    "black-forest-labs/FLUX.1-dev",
    torch_dtype=torch.float16
)

# Komponenten werden automatisch geladen:
# - text_encoder: CLIP-L
# - text_encoder_2: T5-XXL (4.7GB!)
# - transformer: Flux DiT
# - vae: FLUX-VAE
```

---

### **Wan Video Modelle - 3D Causal VAE:**
```
┌─────────────────────────────────────┐
│ Wan Video Architecture (14B params) │
├─────────────────────────────────────┤
│ ✅ CLIP Text Encoder                │
│ ✅ T5 Text Encoder                  │
│ ✅ Diffusion Transformer (Video)    │
│ ✅ Wan-VAE (3D Causal VAE!)         │
└─────────────────────────────────────┘

Komponenten:
1. Text Encoders:
   - CLIP für globales Verständnis
   - T5 für detaillierte Prompts

2. Wan-VAE (3D Causal):
   - Model ID: wangkanai/wan22-vae
   - Speziell für Video-Generierung
   - 3D Causal Architecture
   - Nicht kompatibel mit Bild-VAEs!

3. Diffusion Transformer:
   - 14 Milliarden Parameter
   - Video-spezifisch
   - 3D Attention Mechanisms

VRAM: 16-24 GB
Generation: 5-15 Minuten pro Video
```

**Hugging Face Pipeline:**
```python
from diffusers import DiffusionPipeline

# Wan 2.1/2.2 korrekte Verwendung:
pipe = DiffusionPipeline.from_pretrained(
    "Wan-AI/Wan2.1-T2V-14B",
    torch_dtype=torch.float16,
    custom_pipeline="text_to_video_wan"  # Spezieller Pipeline!
)

# Separate VAE laden:
from diffusers import AutoencoderKL
vae = AutoencoderKL.from_pretrained(
    "wangkanai/wan22-vae",
    torch_dtype=torch.float16
)
pipe.vae = vae
```

---

### **Qwen-VL Modelle - Vision-Language:**
```
┌─────────────────────────────────────┐
│ Qwen-VL Architecture (7B params)    │
├─────────────────────────────────────┤
│ ✅ Vision Encoder (ViT)             │
│ ✅ Qwen2.5 Language Model           │
│ ✅ Cross-Attention Layers           │
│ ✅ Image Tokenizer (eigener!)       │
└─────────────────────────────────────┘

Komponenten:
1. Vision Encoder:
   - Vision Transformer (ViT)
   - Verarbeitet Bilder zu Visual Tokens

2. Language Model:
   - Qwen2.5-7B Base Model
   - SentencePiece Tokenizer!
   - Nicht CLIP/T5!

3. Image Generation Module:
   - Qwen-Image spezifischer Decoder
   - Text-Rendering Spezialist
   - Eigene VAE

VRAM: 8-16 GB
Besonderheit: Chinesisch + Englisch
```

**Hugging Face Pipeline:**
```python
from transformers import Qwen2VLForConditionalGeneration

# Qwen-VL korrekte Verwendung:
model = Qwen2VLForConditionalGeneration.from_pretrained(
    "Qwen/Qwen2.5-VL-7B-Instruct",
    torch_dtype=torch.float16
)

# Eigener Tokenizer erforderlich!
from transformers import AutoTokenizer
tokenizer = AutoTokenizer.from_pretrained(
    "Qwen/Qwen2.5-VL-7B-Instruct"
)
```

---

## 🔧 Implementierungs-Anforderungen

### **Problem: Unser aktueller Code**

```python
# FALSCH für FLUX/Wan/Qwen:
"flux-dev": {
    "pipeline_class": DiffusionPipeline,  # Zu generisch!
    "img2img_class": None,
    "type": "text2img"
}
```

**Was fehlt:**
- ❌ Keine speziellen Pipeline-Klassen
- ❌ Keine VAE-Konfiguration
- ❌ Keine Text Encoder Konfiguration
- ❌ Keine T5-XXL Download-Warnung

---

## ✅ Korrekte Implementierung

### **FLUX.1 Models:**

```python
from diffusers import FluxPipeline, FluxImg2ImgPipeline

AVAILABLE_MODELS = {
    "flux-dev": {
        "name": "FLUX.1 Dev",
        "model_id": "black-forest-labs/FLUX.1-dev",
        "pipeline_class": FluxPipeline,
        "img2img_class": FluxImg2ImgPipeline,
        "type": "text2img",
        "requires_auth": True,  # Gated model!
        "components": {
            "text_encoder": "openai/clip-vit-large-patch14",
            "text_encoder_2": "google/t5-v1_1-xxl",  # 4.7GB!
            "vae": "black-forest-labs/FLUX.1-dev/vae",
            "transformer": "black-forest-labs/FLUX.1-dev/transformer"
        },
        "vram_required": 24,  # Minimum!
        "warning": "FLUX requires 24GB+ VRAM and HuggingFace login"
    }
}
```

---

### **Wan Video Models:**

```python
from diffusers import DiffusionPipeline
from diffusers import AutoencoderKL

AVAILABLE_MODELS = {
    "wan22-t2v": {
        "name": "Wan 2.2 T2V 14B",
        "model_id": "Wan-AI/Wan2.2-T2V-14B",
        "pipeline_class": DiffusionPipeline,
        "custom_pipeline": "text_to_video_wan",
        "type": "text2video",
        "components": {
            "vae": "wangkanai/wan22-vae",  # 3D Causal VAE!
            "text_encoder": "clip",
            "text_encoder_2": "t5"
        },
        "vram_required": 16,
        "generation_time": "5-15 minutes",
        "warning": "Video generation is experimental and very slow"
    }
}

# Spezielle Lade-Logik:
def load_wan_model(model_key):
    pipe = DiffusionPipeline.from_pretrained(
        model_info["model_id"],
        custom_pipeline="text_to_video_wan",
        torch_dtype=torch.float16
    )
    
    # Separate VAE laden:
    vae = AutoencoderKL.from_pretrained(
        "wangkanai/wan22-vae",
        torch_dtype=torch.float16
    )
    pipe.vae = vae
    
    return pipe
```

---

### **Qwen Models:**

```python
from transformers import (
    Qwen2VLForConditionalGeneration,
    AutoTokenizer,
    AutoProcessor
)

AVAILABLE_MODELS = {
    "qwen": {
        "name": "Qwen-Image",
        "model_id": "Qwen/Qwen2.5-VL-7B-Instruct",
        "pipeline_class": Qwen2VLForConditionalGeneration,
        "type": "text2img",
        "components": {
            "tokenizer": "Qwen/Qwen2.5-VL-7B-Instruct",
            "processor": "Qwen/Qwen2.5-VL-7B-Instruct"
        },
        "vram_required": 8,
        "special_features": [
            "Text rendering in images",
            "Chinese + English support",
            "Custom tokenizer required"
        ]
    }
}

# Spezielle Lade-Logik:
def load_qwen_model(model_key):
    model = Qwen2VLForConditionalGeneration.from_pretrained(
        model_info["model_id"],
        torch_dtype=torch.float16
    )
    
    tokenizer = AutoTokenizer.from_pretrained(
        model_info["model_id"]
    )
    
    processor = AutoProcessor.from_pretrained(
        model_info["model_id"]
    )
    
    return model, tokenizer, processor
```

---

## 📦 Requirements Update

### **Zusätzliche Dependencies erforderlich:**

```python
# requirements.txt muss erweitert werden:

# FLUX.1 Support
transformers>=4.44.0  # Für T5-XXL Support
accelerate>=0.33.0    # Für große Modelle

# Wan Video Support
# (Bereits mit diffusers abgedeckt)
# Aber: Separate VAE Download erforderlich!

# Qwen Support
sentencepiece>=0.2.1  # ✅ Bereits vorhanden
protobuf==5.28.3      # ✅ Bereits vorhanden
transformers>=4.44.0  # Für Qwen2.5-VL

# Empfohlen für große Modelle:
bitsandbytes>=0.43.0  # Für 8-bit/4-bit Quantization
```

---

## ⚠️ VRAM & Download-Warnungen

### **FLUX.1 Dev:**
```
Total Download: ~35 GB
├── FLUX Transformer: ~23 GB
├── T5-XXL Encoder: ~10 GB
├── CLIP-L Encoder: ~1 GB
└── FLUX-VAE: ~1 GB

VRAM Usage:
├── FP16: ~22-24 GB
├── INT8: ~12-14 GB (mit bitsandbytes)
└── INT4: ~8-10 GB (mit bitsandbytes)
```

### **Wan 2.2 Models:**
```
Total Download: ~25 GB
├── Wan Transformer: ~20 GB
├── Wan-VAE: ~3 GB
├── Text Encoders: ~2 GB

VRAM Usage:
├── Video Generation: ~18-22 GB
├── Image-to-Video: ~16-20 GB
└── Generation Time: 5-15 minutes!
```

### **Qwen Models:**
```
Total Download: ~14 GB
├── Qwen2.5-7B Model: ~13 GB
├── Vision Encoder: ~1 GB

VRAM Usage:
├── FP16: ~14-16 GB
└── INT8: ~8-10 GB
```

---

## 🚧 Aktuelle Einschränkungen

### **Was NICHT funktioniert (noch):**

1. **FLUX.1 Models:**
   - ❌ Aktueller Code lädt nur generisches `DiffusionPipeline`
   - ❌ T5-XXL wird nicht automatisch geladen
   - ❌ FLUX-VAE nicht konfiguriert
   - ❌ Keine Hugging Face Auth-Prüfung

2. **Wan Video Models:**
   - ❌ Kein `custom_pipeline` Parameter
   - ❌ Wan-VAE wird nicht separat geladen
   - ❌ Keine Video-Output-Handling
   - ❌ UI zeigt keine Video-Preview

3. **Qwen Models:**
   - ❌ Verwendet falsche Pipeline-Klasse
   - ❌ Kein SentencePiece Tokenizer geladen
   - ❌ Kein Processor konfiguriert
   - ❌ Image-Edit-Logik fehlt

---

## ✅ Empfohlene Vorgehensweise

### **Kurzfristig (v1.7.1):**
```
1. Dokumentation aktualisieren:
   ✅ ADVANCED_MODELS_ARCHITECTURE.md (diese Datei)
   ✅ Warnungen in README.md
   ✅ "Experimentell" Status für FLUX/Wan/Qwen

2. UI-Warnung hinzufügen:
   - "Dieses Modell benötigt spezielle Komponenten"
   - "Download-Größe: XX GB"
   - "VRAM erforderlich: XX GB"
   - "Hugging Face Login erforderlich" (FLUX)

3. Modelle als "Advanced" markieren:
   - Separate Kategorie in der UI
   - Klare Warnung vor dem Laden
```

### **Mittelfristig (v1.8.0):**
```
1. Spezielle Pipeline-Loader:
   - load_flux_model()
   - load_wan_model()
   - load_qwen_model()

2. Komponenten-Management:
   - Automatischer VAE-Download
   - Text Encoder Verwaltung
   - VRAM-Check vor dem Laden

3. UI-Verbesserungen:
   - Video-Player für Wan-Outputs
   - Download-Progress für große Modelle
   - VRAM-Usage Anzeige
```

### **Langfristig (v2.0):**
```
1. Vollständige Integration:
   - Alle Komponenten automatisch
   - Optimierte Pipelines
   - Quantization-Support (8-bit/4-bit)

2. Video-Generation:
   - Dedicated Video Tab
   - Timeline-Editor
   - Frame-by-Frame Preview

3. Model-Varianten:
   - FLUX.1 schnell/dev/pro
   - Wan distilled models
   - Qwen verschiedene Größen
```

---

## 🎯 Für Entwickler

### **Wenn Du diese Modelle nutzen willst:**

#### **FLUX.1:**
```python
# Schritt 1: Hugging Face Login
from huggingface_hub import login
login(token="hf_...")

# Schritt 2: FLUX Pipeline laden
from diffusers import FluxPipeline
pipe = FluxPipeline.from_pretrained(
    "black-forest-labs/FLUX.1-dev",
    torch_dtype=torch.float16
).to("cuda")

# Schritt 3: Generieren
image = pipe(
    "a cat",
    num_inference_steps=20,
    guidance_scale=3.5
).images[0]
```

#### **Wan 2.2:**
```python
# Schritt 1: Pipeline laden
from diffusers import DiffusionPipeline
pipe = DiffusionPipeline.from_pretrained(
    "Wan-AI/Wan2.2-T2V-14B",
    custom_pipeline="text_to_video_wan",
    torch_dtype=torch.float16
).to("cuda")

# Schritt 2: VAE laden
from diffusers import AutoencoderKL
vae = AutoencoderKL.from_pretrained(
    "wangkanai/wan22-vae",
    torch_dtype=torch.float16
).to("cuda")
pipe.vae = vae

# Schritt 3: Video generieren
video = pipe(
    "a cat playing",
    num_frames=120,  # 5 Sekunden @ 24fps
    num_inference_steps=30
).frames
```

#### **Qwen:**
```python
# Schritt 1: Model und Tokenizer laden
from transformers import (
    Qwen2VLForConditionalGeneration,
    AutoTokenizer
)

model = Qwen2VLForConditionalGeneration.from_pretrained(
    "Qwen/Qwen2.5-VL-7B-Instruct",
    torch_dtype=torch.float16
).to("cuda")

tokenizer = AutoTokenizer.from_pretrained(
    "Qwen/Qwen2.5-VL-7B-Instruct"
)

# Schritt 2: Generieren
inputs = tokenizer("Generate an image of a cat", return_tensors="pt")
outputs = model.generate(**inputs)
image = decode_qwen_output(outputs)
```

---

## 📚 Weiterführende Links

### **FLUX.1:**
- Hugging Face: https://huggingface.co/black-forest-labs/FLUX.1-dev
- Diffusers Docs: https://huggingface.co/docs/diffusers/api/pipelines/flux
- Architecture Paper: https://arxiv.org/html/2507.09595v1

### **Wan:**
- GitHub: https://github.com/Wan-Video/Wan2.2
- Hugging Face: https://huggingface.co/Wan-AI
- VAE: https://huggingface.co/wangkanai/wan22-vae

### **Qwen:**
- GitHub: https://github.com/QwenLM/Qwen-Image
- Hugging Face: https://huggingface.co/Qwen/Qwen2.5-VL-7B-Instruct
- Docs: https://qwenlm.github.io/

---

**Version:** v1.7.1  
**Status:** 🚧 Experimentelle Unterstützung - Spezielle Konfiguration erforderlich!  
**Letzte Aktualisierung:** 2025-01-20
