# Astroburner-UI - Desktop AI Generation App

Eine moderne Desktop-Anwendung für KI-basierte Bild- und Videogenerierung mit lokalem GPU-Support.

![Astroburner-UI](https://img.shields.io/badge/version-1.9.0-blue)
![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey)
![License](https://img.shields.io/badge/license-MIT-green)

## 🎯 Features

### v1.9.0 Major Update (NEU!)
- 🎨 **Custom Model Integration** - Eigene .safetensors Modelle hochladen
- 🤖 **Automatische Typ-Erkennung** - Erkennt SD1.5, SDXL, FLUX automatisch aus Tensor-Struktur
- 🎯 **Manuelle Klassifizierung** - 14 Model-Typen manuell zuordnen (SD1.5, SDXL, FLUX, etc.)
- 🔢 **Präzisions-Support** - FP32, FP16, BF16, FP8 Safetensors werden unterstützt
- 🖼️ **Optional Thumbnail** - Vorschaubilder für Custom Models hinzufügen
- 📂 **Custom Model Management** - Liste, Löschen, Aktivieren von Custom Models
- 🔍 **Metadata-Analyse** - Automatische Analyse von Tensor-Keys und Model-Metadata

### v1.8.0 Features (Previous Release)
- 🎨 **History Copy-Funktion** - Einstellungen direkt aus History übernehmen
- 💚 **Model Download Indicator** - Grünes Licht für heruntergeladene Modelle
- ⚡ **LoRA Strength -1 bis +2** - Negativer Range für inverse LoRAs
- 🔞 **NSFW Toggle** - Safety Checker aktivieren/deaktivieren
- 🎯 **Generate Button im Header** - Zentral platziert für bessere UX
- 🏷️ **Neuer Name: Astroburner-UI** - Konsistentes Branding

### v1.7.5 Bugfixes
- 🐛 **LoRA Durchsuchen-Button** - Dialog-Plugin jetzt voll funktionsfähig
- 🐛 **LoRA Persistenz** - LoRAs verschwinden nicht mehr nach Page-Refresh
- 🐛 **History Prompt-Anzeige** - Positive Prompts werden nicht mehr abgeschnitten
- 🐛 **Seed-Anzeige** - Seeds werden jetzt korrekt in History angezeigt
- 🐛 **Auto-Resize Textareas** - Prompt-Felder passen sich automatisch der Textlänge an

### v1.7.1 Features
- 🆕 **11 neue Modelle hinzugefügt:**
  - **Pony Diffusion XL V6** ✅ - Anthropomorphe Charaktere (SDXL-kompatibel)
  - **Illustrious XL** ✅ - High-Quality Anime (SDXL-kompatibel)
  - **FLUX.1 Dev** 🚧 - Hochauflösende Bilder (24GB VRAM, spezielle Architektur)
  - **FLUX.1 Kontext Dev** 🚧 - Instruction-based Image Editing (spezielle Architektur)
  - **Wan 2.1 T2V 14B** 🚧 - Text-to-Video Generation (experimentell)
  - **Wan 2.1 I2V 14B** 🚧 - Image-to-Video Generation (experimentell)
  - **Wan 2.2 T2V 14B** 🚧 - Enhanced Text-to-Video (experimentell)
  - **Wan 2.2 I2V 14B** 🚧 - Enhanced Image-to-Video (experimentell)
  - **Wan 2.2 S2V 14B** 🚧 - Speech-to-Video Generation (experimentell)
  - **Qwen-Image** 🚧 - Text-Rendering & Poster (spezielle Architektur)
  - **Qwen-Image Edit** 🚧 - Präzise Bildbearbeitung (spezielle Architektur)
- ✅ **LoRA Support** für alle SDXL-basierten Modelle (SD1.5, SDXL, Pony, Illustrious)
- ✅ **Automatische Dialog Plugin Integration** für File-Picker
- ✅ **CUDA Auto-Detection & Auto-Fix** für RTX 5090

**⚠️ WICHTIGER HINWEIS:** FLUX, Wan und Qwen verwenden **spezielle Architekturen** mit eigenen VAEs, Text Encodern und Komponenten. Siehe `ADVANCED_MODELS_ARCHITECTURE.md` für Details. Diese Modelle benötigen manuelle Konfiguration in v1.7.1!

### v1.6.0 Features
- ✅ **Text-to-Image Generation** mit mehreren Parametern
- ✅ **Image-to-Image** mit Denoise Strength Control
- ✅ **Multi-Model Support** (SD1.5, SDXL, SDXL-Turbo)
- ✅ **Complete LoRA Management** (bis zu 5 gleichzeitig)
- ✅ **Individual LoRA Strength Control** (0.0-2.0)
- ✅ **GPU Management** mit VRAM Monitoring
- ✅ **Enhanced History Panel** mit Scheduler & Denoise Display
- ✅ **Modern Dark UI** mit Tailwind CSS
- ✅ **Lazy Model Loading** für optimierte Performance
- ✅ **SQLite Database** für Metadata & History

### Geplant (Future)
- 🔄 Text-to-Video Generation (Wan Model)
- 🔄 Inpainting & Outpainting
- 🔄 ControlNet Support
- 🔄 Batch Processing
- 🔄 Model Download Manager

## 🏗️ Tech Stack

### Frontend
- **Framework:** Tauri 2.0 (Rust + Web)
- **UI Library:** React 18 + TypeScript
- **Styling:** Tailwind CSS
- **State Management:** Zustand
- **Icons:** React Icons

### Backend
- **Framework:** FastAPI (Python)
- **ML Framework:** PyTorch + Diffusers
- **Database:** SQLite (aiosqlite)
- **GPU Support:** CUDA (NVIDIA), MPS (Apple Silicon)

## 📋 Voraussetzungen

### ⚠️ Erforderliche Software (MUSS installiert sein!)

Bevor du `setup.bat` ausführst, installiere bitte folgende Software:

#### Windows:
1. **Python 3.10 oder 3.11** - [Download](https://www.python.org/downloads/)
   - ⚠️ Bei Installation: "Add Python to PATH" aktivieren!
2. **Node.js 18+ (LTS)** - [Download](https://nodejs.org/)
3. **Git** - [Download](https://git-scm.com/downloads)
4. **Visual Studio Build Tools** (für Rust) - [Download](https://visualstudio.microsoft.com/de/visual-cpp-build-tools/)
   - Wähle: "Desktop development with C++"
5. **Rust** - [Download](https://rustup.rs/)
   - Nach Installation: Terminal neu starten

#### macOS:
```bash
# Mit Homebrew
brew install python@3.11 node git rust
```

#### Linux (Ubuntu/Debian):
```bash
sudo apt update
sudo apt install python3.11 python3.11-venv nodejs npm git build-essential
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
```

### Hardware
- **GPU:** NVIDIA GPU mit CUDA Support (empfohlen 6GB+ VRAM)
  - RTX 5090/50-series: CUDA 12.8 (automatisch erkannt)
  - RTX 4090/40-series: CUDA 12.1
  - RTX 3090/30-series: CUDA 11.8
  - Alternativ: Apple Silicon (MPS) oder CPU (langsam)
- **RAM:** Mindestens 16GB (32GB empfohlen für große Modelle)
- **Speicher:** 30GB+ freier Speicherplatz für Models und Installation

## 🚀 Installation & Start

### ⚡ Automatische Installation mit setup.bat (EMPFOHLEN!)

**Ein einziger Befehl installiert alles automatisch!**

```cmd
<<<<<<< HEAD
# 1. Download und entpacken
# https://github.com/Astroburner/AStroburner-UI.git

# 2. Automatische Installation (15-25 Min)
cd AStroburner-UI
=======
# 1. Repository klonen
git clone https://github.com/Astroburner/AStroburner-UI.git
cd AStroburner-UI

# 2. Setup ausführen (15-25 Min)
>>>>>>> 5ead5ea (v1.7.5: Critical Bugfixes - LoRA, History, Prompts)
setup.bat

# 3. GPU-Auswahl während Installation:
#    Option 1: RTX 5090 / RTX 50-series (CUDA 12.8) [AUTO-DETECTED]
#    Option 2: RTX 4090 / RTX 40-series (CUDA 12.1)
#    Option 3: RTX 3090 / RTX 30-series (CUDA 11.8)
#    Option 4: CPU only
```

### Was macht setup.bat?

✅ **Automatische CUDA-Erkennung** - Erkennt deine GPU (RTX 5090) automatisch
✅ **Python Virtual Environment** - Erstellt isolierte Python-Umgebung
✅ **PyTorch mit CUDA** - Installiert korrekte CUDA-Version (12.8 für RTX 5090)
✅ **Backend Dependencies** - Installiert alle Python-Pakete aus requirements.txt
✅ **Frontend Dependencies** - Installiert Node.js Pakete (React, Tauri)
✅ **CUDA-Verifizierung** - Prüft ob PyTorch CUDA nutzen kann
✅ **Automatischer CUDA-Fix** - Repariert PyTorch automatisch bei CPU-Fallback
✅ **Interaktives Menü** - Zeigt Quick Actions nach Installation

**Das war's! 🎉**

### Nach der Installation: App starten

```cmd
# Option 1: Mit setup.bat Menü
setup.bat
# → Wähle "1) Start App (Backend + Frontend)"

<<<<<<< HEAD
Falls du setup.bat nicht nutzen möchtest, folge dieser Anleitung:

### 1. Repository Klonen

```bash
git clone https://github.com/Astroburner/AStroburner-UI.git
cd ai-studio
```

### 2. Backend Setup (Python)

```bash
=======
# Option 2: Manuell
>>>>>>> 5ead5ea (v1.7.5: Critical Bugfixes - LoRA, History, Prompts)
cd backend
venv\Scripts\activate
python main.py
# In neuem Terminal:
cd frontend
npm run tauri dev
```

---

## 🎮 Manuelle Installation (Fortgeschritten)

**Nur wenn setup.bat nicht funktioniert!**

Siehe [CONTRIBUTING.md](CONTRIBUTING.md) für detaillierte manuelle Installation.

## 📖 Verwendung

### Erste Schritte

1. **App starten** - Backend und Frontend müssen beide laufen
2. **Model laden** - Gehe zu Settings → Models → "SDXL Turbo" laden (schnellstes Model)
3. **Prompt eingeben** - Beschreibe was du generieren möchtest
4. **Parameter anpassen** - Width, Height, Steps, Guidance Scale
5. **Generate** - Klicke "Bild Generieren"

### Parameter Erklärung

- **Width/Height:** Bildgröße (512x512 = schnell, 1024x1024 = hochauflösend)
- **Steps:** Anzahl Diffusions-Steps (20-30 = schnell, 50+ = hohe Qualität)
- **Guidance Scale:** Wie stark der Prompt befolgt wird (7-8 = ausgewogen, 12+ = sehr streng)
- **Seed:** Für reproduzierbare Ergebnisse (leer = random)

### Empfohlene Einstellungen

**Schnelle Generierung:**
- Model: SDXL-Turbo
- Size: 512x512
- Steps: 4-8
- Guidance: 0-1

**Hohe Qualität:**
- Model: SDXL Base
- Size: 1024x1024
- Steps: 30-50
- Guidance: 7-8

## 🗂️ Projektstruktur

```
ai-studio/
├── backend/                 # Python FastAPI Backend
│   ├── api/                # API Routes
│   ├── core/               # Core Funktionen (GPU, Model Manager)
│   ├── models/             # Database Models
│   ├── utils/              # Utilities
│   ├── config.py           # Configuration
│   ├── main.py             # FastAPI App Entry
│   └── requirements.txt    # Python Dependencies
│
├── frontend/               # React + Tauri Frontend
│   ├── src/
│   │   ├── components/    # React Components
│   │   ├── hooks/         # Custom Hooks (Zustand Store)
│   │   ├── services/      # API Service
│   │   ├── types/         # TypeScript Types
│   │   └── styles/        # Tailwind CSS
│   ├── src-tauri/         # Tauri Rust Backend
│   │   ├── src/          # Rust Source
│   │   └── tauri.conf.json
│   ├── package.json
│   └── vite.config.ts
│
├── models/                 # AI Models (auto-downloaded)
├── outputs/                # Generated Images
├── ai_studio.db           # SQLite Database
└── README.md
```

## 🐛 Troubleshooting

### Backend startet nicht

**Problem:** `ModuleNotFoundError: No module named 'torch'`
```bash
# Virtual Environment aktivieren!
source venv/bin/activate  # oder venv\Scripts\activate
pip install -r requirements.txt
```

**Problem:** CUDA nicht gefunden
```bash
# Check CUDA Installation:
nvidia-smi

# PyTorch mit CUDA neu installieren:
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu121
```

### Frontend baut nicht

**Problem:** Tauri CLI fehlt
```bash
npm install --save-dev @tauri-apps/cli
```

**Problem:** Rust fehlt
- Installiere Rust: https://rustup.rs/

### Models downloaden langsam

- Models werden beim ersten Laden automatisch von HuggingFace heruntergeladen
- SDXL Base: ~6.9GB
- SDXL Turbo: ~6.9GB
- SD 1.5: ~4GB

Cache Location: `models/` Ordner

### VRAM Fehler (Out of Memory)

**Lösung 1:** Kleinere Bildgröße verwenden (512x512)
**Lösung 2:** Weniger Steps (20-30)
**Lösung 3:** Settings → GPU Cache Leeren

## 🔧 API Dokumentation

Backend API läuft auf: `http://127.0.0.1.9.00`

### Endpoints

- `GET /api/health` - Health Check
- `GET /api/gpu/info` - GPU Informationen
- `POST /api/gpu/clear-cache` - GPU Cache leeren
- `GET /api/models` - Verfügbare Models auflisten
- `POST /api/models/load` - Model laden
- `POST /api/generate/image` - Bild generieren
- `GET /api/history` - Generation History
- `GET /api/stats` - Statistiken

API Docs: http://127.0.0.1.9.00/docs (Swagger UI)

## 📊 Performance

### Benchmark (NVIDIA RTX 3080)

| Model | Size | Steps | Time |
|-------|------|-------|------|
| SD 1.5 | 512x512 | 30 | ~8s |
| SDXL Base | 1024x1024 | 30 | ~25s |
| SDXL Turbo | 512x512 | 4 | ~2s |

## 🤝 Contributing

Contributions sind willkommen! Bitte erstelle ein Issue oder Pull Request.

## 📝 License

MIT License - siehe LICENSE Datei

## 👤 Autor

**Astroburner**
- YouTube: [@Astroburner-AI](https://www.youtube.com/@Astroburner-AI)
- GitHub: [@Astroburner](https://github.com/Astroburner)

## 🙏 Credits

- Stable Diffusion by Stability AI
- Diffusers by HuggingFace
- Tauri Framework
- React & Tailwind CSS

---

**Viel Spaß beim Generieren! 🎨✨**
