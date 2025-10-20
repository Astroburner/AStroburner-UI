# Changelog

All notable changes to AI Studio will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [1.9.0] - 2025-01-20

### 🎉 Features (Custom Model Integration)
- **Custom Model Upload** - Eigene .safetensors Modelle hinzufügen
- **Automatische Typ-Erkennung** - Erkennt SD1.5, SDXL, FLUX automatisch
- **Präzisions-Support** - FP32, FP16, BF16, FP8 Safetensors unterstützt
- **Model Type Selection** - Manuelle Zuordnung möglich (SD1.5, SDXL, Pony, etc.)
- **Optional Thumbnail** - Vorschaubilder für Custom Models
- **Custom Model Management** - Liste, Löschen, Aktivieren von Custom Models

### 🔧 Backend
- Database: `custom_models` Tabelle für Custom Models
- API: `/api/custom-models` Endpoints (POST, GET, DELETE)
- API: `/api/custom-models/detect` - Auto-Detection von Model Type
- Utility: `model_detector.py` - Erkennt Model Typ aus Safetensors Metadata
- Support: Alle Präzisionen (FP32/FP16/BF16/FP8)

### 🎨 Frontend
- Component: `CustomModelAddForm` - Upload UI mit Auto-Detection
- Component: `CustomModelList` - Verwaltung der Custom Models
- Settings: Neuer "Custom Models" Tab
- File Picker: .safetensors + Thumbnail (PNG/JPG/WEBP)

### 📚 Documentation
- CHANGELOG.md: v1.9.0 dokumentiert
- README.md: Custom Models Feature hinzugefügt

---

## [1.8.0] - 2025-01-20

### 🎉 Features (Major UI/UX Update)
- **History Copy-Funktion** - Einstellungen direkt aus History in Generate übernehmen (Copy-Button)
- **Settings: Model Download Indicator** - Grünes Licht zeigt heruntergeladene Modelle an
- **LoRA Strength erweitert** - Range von -1 bis +2 (statt 0-2) für mehr Kontrolle
- **NSFW Toggle** - Activate/Deactivate Button für NSFW-Content (Safety Checker)
- **Generate Button verlegt** - Jetzt prominent in Header-Mitte für bessere UX
- **Umbenennung zu "Astroburner-UI"** - Neuer Name im gesamten Projekt

### 🔧 Changed
- Header: Generate-Button in die Mitte verlegt
- LoRA Weights: Negativer Range (-1.0 bis +2.0) für inverse LoRAs
- UI: Konsistentes "Astroburner-UI" Branding

### 📚 Documentation
- README.md: Titel auf "Astroburner-UI" geändert
- package.json: Name auf "astroburner-ui-frontend"
- Tauri Config: Product Name & Identifier aktualisiert

---

## [1.7.5] - 2025-01-20

### 🐛 Fixed (Critical Bugfixes)
- **LoRA Durchsuchen-Button defekt** - Dialog Plugin jetzt voll funktionsfähig
- **LoRAs verschwinden nach Refresh** - Auto-Reload alle Sekunde implementiert
- **History: Positiv-Prompt wird abgeschnitten** - Vollständige Anzeige mit word-wrap
- **History: Seed wird nicht angezeigt** - Seeds werden jetzt korrekt angezeigt (oder "Random")
- **Prompt-Textareas passen sich nicht an** - Auto-Resize basierend auf Textlänge

### 🔧 Changed
- README.md: Fokus auf setup.bat, manuelle Installation in CONTRIBUTING.md
- README.md: Voraussetzungen klar definiert (Python, Node.js, Git, Rust, Visual Studio Build Tools)
- README.md: Installation vereinfacht - nur setup.bat erklärt
- README.md: GitHub Link hinzugefügt

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
