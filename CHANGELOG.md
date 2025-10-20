# Changelog

All notable changes to AI Studio will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [1.7.1] - 2025-01-20

### 🆕 Added
- **11 neue Modelle:**
  - Pony Diffusion XL V6 - Anthropomorphe Charaktere (✅ Ready)
  - Illustrious XL - High-Quality Anime (✅ Ready)
  - FLUX.1 Dev - State-of-the-art T2I (🚧 Experimentell)
  - FLUX.1 Kontext Dev - Image Editing (🚧 Experimentell)
  - Wan 2.1 T2V/I2V - Video Generation (🚧 Experimentell)
  - Wan 2.2 T2V/I2V/S2V - Enhanced Video (🚧 Experimentell)
  - Qwen-Image/Edit - Text Rendering (🚧 Experimentell)
- Dialog Plugin für File Picker (Tauri)
- CUDA Auto-Detection für RTX 5090/4090/3090
- Automatischer CUDA-Fix in setup.bat
- `ADVANCED_MODELS_ARCHITECTURE.md` - Technische Dokumentation
- `NEW_MODELS_v1.7.1.md` - Modell-Übersicht
- GitHub Issue Templates
- CONTRIBUTING.md

### 🔧 Changed
- `sentencepiece` Version: `==0.2.0` → `>=0.2.1`
- Backend Version: 1.6.0 → 1.7.1
- Frontend Version: 1.6.0 → 1.7.1
- setup.bat: EnableDelayedExpansion Syntax korrigiert
- README.md: Status-Icons für Modelle (✅/🚧)

### 🐛 Fixed
- Dialog Plugin Import Error im Frontend
- Pydantic `model_type` namespace Warnung
- Batch-Datei Syntax-Fehler mit "."
- PyTorch CPU-Installation statt CUDA
- Port 3000 Konflikt-Management

### ⚠️ Known Issues
- FLUX/Wan/Qwen benötigen spezielle Konfiguration (siehe ADVANCED_MODELS_ARCHITECTURE.md)
- Video-Generierung ist experimentell und sehr langsam
- FLUX benötigt Hugging Face Login

---

## [1.6.0] - 2025-01-15

### 🆕 Added
- Text-to-Image Generation mit mehreren Parametern
- Image-to-Image mit Denoise Strength Control
- Multi-Model Support (SD1.5, SDXL, SDXL-Turbo)
- Complete LoRA Management (bis zu 5 gleichzeitig)
- Individual LoRA Strength Control (0.0-2.0)
- GPU Management mit VRAM Monitoring
- Enhanced History Panel
- Modern Dark UI mit Tailwind CSS
- Lazy Model Loading
- SQLite Database für Metadata

### 🔧 Changed
- Complete UI Redesign
- Performance Optimierungen
- VRAM Management verbessert

---

## [1.5.0] - 2025-01-10

### 🆕 Added
- Erstes öffentliches Release
- SD1.5 Support
- SDXL Support
- Basic UI

---

## Roadmap

### [1.8.0] - Geplant
- ✅ Vollständige FLUX.1 Integration mit T5-XXL
- ✅ Wan-VAE automatischer Download
- ✅ Qwen korrekte Pipeline
- ✅ Spezielle Pipeline-Loader
- ✅ VRAM-Check vor Model-Loading
- ✅ UI-Warnungen für große Downloads

### [2.0.0] - Zukunft
- ✅ Video-Tab mit Timeline-Editor
- ✅ Quantization-Support (8-bit/4-bit)
- ✅ Model-Varianten (FLUX schnell/dev/pro)
- ✅ ControlNet Support
- ✅ Inpainting & Outpainting
- ✅ Batch Processing

---

**Legend:**
- 🆕 Added - Neue Features
- 🔧 Changed - Änderungen an existierenden Features
- 🐛 Fixed - Bug Fixes
- ⚠️ Known Issues - Bekannte Probleme
- 🗑️ Removed - Entfernte Features
