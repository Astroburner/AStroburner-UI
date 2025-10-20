# AI Studio v1.7.1 - New Models Documentation

## 🎉 Neue Modelle

AI Studio v1.7.1 fügt **11 neue Modelle** hinzu, die verschiedene Stile und Anwendungsfälle abdecken:

---

## 📋 Modellübersicht

### **1. Pony Diffusion XL V6** 🐴
- **Model ID:** `LyliaEngine/Pony_Diffusion_V6_XL`
- **Typ:** Text-to-Image (SDXL-basiert)
- **Spezialisierung:** Anime, Furry, Anthro-Charaktere
- **VRAM:** 8-12 GB
- **Auflösung:** 1024x1024 (native SDXL)
- **Besonderheiten:**
  - Hervorragend für anthropomorphe Charaktere
  - SFW und NSFW Inhalte möglich
  - Sehr detailliert bei Fell/Texturen
- **Empfohlene Settings:**
  - Steps: 25-35
  - Guidance Scale: 7.0-8.5
  - Scheduler: Euler Ancestral

---

### **2. Illustrious XL** ✨
- **Model ID:** `OnomaAIResearch/Illustrious-xl-early-release-v0`
- **Typ:** Text-to-Image (SDXL-basiert)
- **Spezialisierung:** High-Quality Anime/Illustration
- **VRAM:** 8-12 GB
- **Auflösung:** 1024x1024
- **Besonderheiten:**
  - Fortsetzung von Kohaku XL Beta 5
  - Sehr sauberer, heller Anime-Stil
  - Ausgezeichnete Charakterkonsistenz
- **Empfohlene Settings:**
  - Steps: 28-40
  - Guidance Scale: 7.0-9.0
  - Scheduler: DPM++ 2M Karras

---

### **3. FLUX.1 Dev** 🌊
- **Model ID:** `black-forest-labs/FLUX.1-dev`
- **Typ:** Text-to-Image
- **Spezialisierung:** Hochauflösende, realistische Bilder
- **VRAM:** 24+ GB (sehr groß!)
- **Auflösung:** Variable (bis 2048x2048)
- **Besonderheiten:**
  - 12 Milliarden Parameter
  - Rectified Flow Transformer
  - State-of-the-art Qualität
  - **WICHTIG:** Gated Model - Hugging Face Login erforderlich!
- **Empfohlene Settings:**
  - Steps: 20-30
  - Guidance Scale: 3.5-5.0
  - Scheduler: Euler

---

### **4. FLUX.1 Kontext Dev** 🎨
- **Model ID:** `black-forest-labs/FLUX.1-Kontext-dev`
- **Typ:** Image-to-Image (Text-gesteuert)
- **Spezialisierung:** Bildbearbeitung nach Anweisungen
- **VRAM:** 24+ GB
- **Auflösung:** Variable
- **Besonderheiten:**
  - Instruction-based Image Editing
  - Kann Bilder gezielt nach Textanweisungen verändern
  - Sehr präzise Kontrolle
  - **WICHTIG:** Gated Model - Hugging Face Login erforderlich!
- **Empfohlene Settings:**
  - Steps: 20-30
  - Guidance Scale: 3.5-5.0
  - Denoise Strength: 0.5-0.8

---

### **5. Wan 2.1 T2V 14B** 🎬
- **Model ID:** `Wan-AI/Wan2.1-T2V-14B`
- **Typ:** Text-to-Video
- **Spezialisierung:** Video-Generierung aus Text
- **VRAM:** 16+ GB
- **Auflösung:** 480p, 720p
- **Besonderheiten:**
  - 14 Milliarden Parameter
  - Hochwertige Video-Generierung
  - Unterstützt beide Auflösungen
  - Alibaba Open-Source Model
- **Hinweis:**
  - Video-Generierung ist experimentell
  - Kann mehrere Minuten pro Video dauern
  - Spezielle Pipeline-Konfiguration erforderlich

---

### **6. Wan 2.1 I2V 14B** 🖼️➡️🎬
- **Model ID:** `Wan-AI/Wan2.1-I2V-14B`
- **Typ:** Image-to-Video
- **Spezialisierung:** Video-Generierung aus Einzelbild
- **VRAM:** 16+ GB
- **Auflösung:** 480p, 720p
- **Besonderheiten:**
  - Animiert statische Bilder zu Videos
  - Hochwertige Bewegungsgenerierung
  - Konsistente Charakterdarstellung
- **Hinweis:**
  - Benötigt Eingabebild
  - Video-Generierung ist experimentell

---

### **7. Wan 2.2 T2V 14B** 🎬
- **Model ID:** `Wan-AI/Wan2.2-T2V-14B`
- **Typ:** Text-to-Video
- **Spezialisierung:** Verbesserte Video-Generierung aus Text
- **VRAM:** 16+ GB
- **Auflösung:** 480p, 720p
- **Besonderheiten:**
  - Neueste Wan-Version (2.2)
  - Bessere Qualität als 2.1
  - Schnellere Inferenz
  - Verbesserte Bewegungsqualität
- **Hinweis:**
  - Empfohlen gegenüber Wan 2.1 T2V
  - Experimentelle Unterstützung

---

### **8. Wan 2.2 I2V 14B** 🖼️➡️🎬
- **Model ID:** `Wan-AI/Wan2.2-I2V-14B`
- **Typ:** Image-to-Video
- **Spezialisierung:** Verbesserte Bild-zu-Video-Konvertierung
- **VRAM:** 16+ GB
- **Auflösung:** 480p, 720p
- **Besonderheiten:**
  - Neueste I2V-Version
  - Natürlichere Bewegungen
  - Bessere Charakterkonsistenz
- **Hinweis:**
  - Empfohlen gegenüber Wan 2.1 I2V
  - Benötigt Eingabebild

---

### **9. Wan 2.2 S2V 14B** 🎤
- **Model ID:** `Wan-AI/Wan2.2-S2V-14B`
- **Typ:** Speech-to-Video
- **Spezialisierung:** Audio-gesteuerte Video-Generierung
- **VRAM:** 16+ GB
- **Auflösung:** 480p, 720p
- **Besonderheiten:**
  - Generiert Videos aus Audiodateien
  - Ideal für Digital Humans / Talking Heads
  - Neueste Version (2.2)
  - Cinematic Video Generation
- **Hinweis:**
  - Benötigt Audioeingabe (.wav, .mp3)
  - Experimentelles Feature

---

### **10. Qwen-Image** 🖼️
- **Model ID:** `Qwen/Qwen-Image`
- **Typ:** Text-to-Image
- **Spezialisierung:** Komplexe Text-Rendering, Poster
- **VRAM:** 8-16 GB
- **Auflösung:** Variable
- **Besonderheiten:**
  - Exzellentes Text-Rendering im Bild
  - Gut für Poster/Designs mit Text
  - Unterstützt Chinesisch und Englisch
  - Apache 2.0 Lizenz
- **Empfohlene Settings:**
  - Steps: 25-35
  - Guidance Scale: 7.0-9.0

---

### **11. Qwen-Image Edit** ✏️
- **Model ID:** `Qwen/Qwen-Image` (gleiche Basis wie Qwen-Image)
- **Typ:** Image-to-Image
- **Spezialisierung:** Präzise Bildbearbeitung
- **VRAM:** 8-16 GB
- **Auflösung:** Variable
- **Besonderheiten:**
  - Instruction-based Editing
  - Kann Text in Bildern bearbeiten
  - Sehr präzise Kontrolle
- **Empfohlene Settings:**
  - Steps: 20-30
  - Denoise Strength: 0.6-0.8

---

## 🔧 Technische Details

### **Pipeline-Kompatibilität:**

| Modell | Pipeline-Typ | Basis |
|--------|-------------|-------|
| Pony Diffusion XL | StableDiffusionXLPipeline | SDXL |
| Illustrious XL | StableDiffusionXLPipeline | SDXL |
| FLUX.1 Dev | DiffusionPipeline | Flux |
| FLUX.1 Kontext | DiffusionPipeline | Flux |
| Wan 2.1 T2V | DiffusionPipeline | Wan |
| Wan 2.1 I2V | DiffusionPipeline | Wan |
| Wan 2.2 T2V | DiffusionPipeline | Wan |
| Wan 2.2 I2V | DiffusionPipeline | Wan |
| Wan 2.2 S2V | DiffusionPipeline | Wan |
| Qwen-Image | DiffusionPipeline | Qwen |
| Qwen-Image Edit | DiffusionPipeline | Qwen |

### **VRAM-Anforderungen:**

- **SDXL-basiert (Pony, Illustrious):** 8-12 GB
- **Flux-basiert:** 24+ GB (sehr groß!)
- **Wan-basiert:** 16+ GB
- **Qwen-basiert:** 8-16 GB

---

## 📦 Installation

### **1. Backend Dependencies aktualisieren:**

```bash
cd backend
venv\Scripts\activate
pip install -r requirements.txt
```

**Neue Dependencies in v1.7.1:**
- `sentencepiece==0.2.0` - Für Qwen Tokenizers
- `protobuf==5.28.3` - Für Qwen und Flux Models

### **2. Hugging Face Login (für Flux):**

Flux-Modelle sind "gated" und benötigen Login:

```bash
huggingface-cli login
```

**Oder in Python:**
```python
from huggingface_hub import login
login(token="your_hf_token_here")
```

Token erstellen: https://huggingface.co/settings/tokens

---

## 🎨 Verwendung in AI Studio

### **Modell laden:**

1. Öffne AI Studio
2. Gehe zu "Models" Tab
3. Wähle das gewünschte Modell:
   - **SD1.5** - Original Stable Diffusion
   - **SDXL** - Stable Diffusion XL
   - **SDXL-Turbo** - Schnelle SDXL-Variante
   - **Pony** - Anthropomorphe Charaktere
   - **Illustrious** - High-Quality Anime
   - **Flux-Dev** - Hochauflösende Bilder
   - **Flux-Kontext** - Bildbearbeitung
   - **Wan2.1** - Video-Generierung
   - **Wan2.2** - Audio-to-Video
   - **Qwen** - Text-Rendering
   - **Qwen-image-edit** - Bildbearbeitung

### **LoRAs mit neuen Modellen:**

LoRAs sind kompatibel mit:
- ✅ **SD1.5** - SD1.5 LoRAs
- ✅ **SDXL** - SDXL LoRAs
- ✅ **Pony** - SDXL LoRAs (optimiert für Pony)
- ✅ **Illustrious** - SDXL LoRAs (optimiert für Illustrious)
- ❌ **Flux** - Keine Standard-LoRA-Unterstützung (eigenes System)
- ❓ **Wan** - Video-LoRAs (experimentell)
- ❓ **Qwen** - Experimentell

**Wichtig:** Wähle den richtigen "Model Type" beim LoRA-Hinzufügen!

---

## ⚠️ Bekannte Einschränkungen

### **Flux-Modelle:**
- Sehr groß (24+ GB VRAM)
- Erfordern Hugging Face Login
- Langsamer als SDXL
- Keine Standard-LoRA-Unterstützung

### **Video-Modelle (Wan):**
- Experimentelle Unterstützung
- Sehr langsam (mehrere Minuten pro Video)
- Hoher VRAM-Bedarf
- UI noch nicht vollständig für Video optimiert

### **Qwen-Modelle:**
- Benötigen spezielle Tokenizer
- Chinesische/Englische Prompts bevorzugt
- Bildbearbeitung experimentell

---

## 🚀 Performance-Tipps

### **Für RTX 5090:**
- ✅ Alle Modelle funktionieren
- ✅ FLUX.1 läuft flüssig (24 GB VRAM)
- ✅ Video-Generierung möglich
- ⚡ Empfohlene Settings:
  - `enable_xformers=True`
  - `enable_attention_slicing=True`
  - `vae_slicing=True`

### **Für RTX 4090 (24 GB):**
- ✅ Alle SDXL-Modelle
- ✅ FLUX.1 läuft (knapp)
- ⚠️ Video-Generierung langsam
- ⚡ Nutze kleinere Batch Sizes

### **Für RTX 3090 (24 GB):**
- ✅ SDXL-Modelle
- ⚠️ FLUX.1 sehr knapp
- ❌ Video-Generierung schwierig
- ⚡ Nutze aggressive VRAM-Optimierungen

### **Für GPUs < 24 GB:**
- ✅ SD1.5, SDXL, Pony, Illustrious
- ❌ FLUX.1 (zu groß)
- ❌ Video-Generierung (zu groß)
- ⚡ Fokus auf SDXL-basierte Modelle

---

## 📚 Weiterführende Links

- **Pony Diffusion:** https://civitai.com/models/257749
- **Illustrious:** https://huggingface.co/OnomaAIResearch/Illustrious-xl-early-release-v0
- **FLUX.1:** https://huggingface.co/black-forest-labs
- **Wan:** https://github.com/Wan-Video
- **Qwen:** https://github.com/QwenLM/Qwen-Image

---

## 🐛 Troubleshooting

### **"Model not found" Fehler:**
```bash
# Cache löschen und neu herunterladen
rm -rf models/
python main.py  # Lädt Modell automatisch neu
```

### **"Out of memory" bei Flux:**
```python
# In config.py:
ENABLE_ATTENTION_SLICING = True
VAE_SLICING = True
```

### **Hugging Face Login Fehler:**
```bash
huggingface-cli login
# Token eingeben: hf_...
```

### **Video-Generierung hängt:**
- Normal! Videos dauern 5-10 Minuten
- Prüfe GPU-Auslastung mit `nvidia-smi`
- Kleinere Auflösung wählen (480p statt 720p)

---

**Version:** v1.7.1  
**Datum:** 2025-01-20  
**Status:** Experimentelle Unterstützung für Video-Modelle
