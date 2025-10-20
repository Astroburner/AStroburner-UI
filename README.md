# AI Studio - Desktop AI Generation App

Eine moderne Desktop-Anwendung für KI-basierte Bild- und Videogenerierung mit lokalem GPU-Support.

![AI Studio](https://img.shields.io/badge/version-1.2.0-blue)
![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey)
![License](https://img.shields.io/badge/license-MIT-green)

## 🎯 Features

### MVP (Version 1.0)
- ✅ **Text-to-Image Generation** mit mehreren Parametern
- ✅ **Multi-Model Support** (SD1.5, SDXL, SDXL-Turbo)
- ✅ **GPU Management** mit VRAM Monitoring
- ✅ **Gallery System** mit History & Metadata
- ✅ **Modern Dark UI** mit Tailwind CSS
- ✅ **Lazy Model Loading** für optimierte Performance
- ✅ **SQLite Database** für Metadata & History

### Geplant (Future)
- 🔄 Text-to-Video Generation (Wan Model)
- 🔄 LoRA Support
- 🔄 Inpainting & Outpainting
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

### Hardware
- **GPU:** NVIDIA GPU mit CUDA Support (empfohlen 6GB+ VRAM)
  - Alternativ: Apple Silicon (MPS) oder CPU (langsam)
- **RAM:** Mindestens 16GB (32GB empfohlen)
- **Speicher:** 20GB+ freier Speicherplatz für Models

### Software
- **Windows:** Windows 10/11 (64-bit)
- **macOS:** macOS 11+ (Apple Silicon oder Intel)
- **Linux:** Ubuntu 20.04+ oder äquivalent

#### Für Entwicklung:
- Node.js 18+ & npm
- Python 3.10+
- Rust 1.70+ (für Tauri)
- Git

## 🚀 Schnellstart (Windows)

### ⚡ Automatische Installation (Empfohlen!)

**NEU in v1.2.0**: Ein einziger Befehl installiert alles automatisch!

```cmd
# 1. Download und entpacken
# https://page.gensparksite.com/project_backups/ai-studio-v1.2.0-interactive-setup.tar.gz

# 2. Automatische Installation (15-25 Min)
cd ai-studio
setup.bat

# 3. Wähle deine GPU während der Installation:
#    Option 1: RTX 5090 / RTX 50-series (CUDA 12.8)
#    Option 2: RTX 4090 / RTX 40-series (CUDA 12.1)
#    Option 3: RTX 3090 / RTX 30-series (CUDA 11.8)
#    Option 4: CPU only
```

**Das war's! 🎉** Nach der Installation zeigt setup.bat ein interaktives Menü mit Quick Actions.

**Siehe:** [SETUP_BAT_README.md](SETUP_BAT_README.md) für Details

---

### 📖 Manuelle Installation

Falls du setup.bat nicht nutzen möchtest, folge dieser Anleitung:

### 1. Repository Klonen

```bash
git clone https://github.com/yourusername/ai-studio.git
cd ai-studio
```

### 2. Backend Setup (Python)

```bash
cd backend

# Virtual Environment erstellen
python -m venv venv

# Aktivieren:
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Dependencies installieren
pip install -r requirements.txt

# PyTorch Installation (wähle basierend auf deiner GPU):

# CUDA 12.8 (RTX 5090, RTX 50-series):
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu128

# CUDA 12.1 (RTX 4090, RTX 40-series):
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu121

# CUDA 11.8 (RTX 3090, RTX 30-series):
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118

# MPS Support (Apple Silicon M1/M2/M3):
pip install torch torchvision

# CPU Only (fallback):
pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu
```

### 3. Frontend Setup (React + Tauri)

```bash
cd ../frontend

# Node Dependencies installieren
npm install

# Rust Dependencies (Tauri CLI)
npm install --save-dev @tauri-apps/cli
```

### 4. Environment Variables (optional)

Erstelle `.env` im Backend-Ordner:

```env
# Backend/.env
DEBUG=True
API_HOST=127.0.0.1
API_PORT=8000
DEVICE=cuda  # cuda, mps, oder cpu
```

## 🎮 Anwendung Starten

### Development Mode

**Terminal 1 - Backend starten:**
```bash
cd backend
source venv/bin/activate  # oder venv\Scripts\activate auf Windows
python main.py
```

Backend läuft auf: `http://127.0.0.1:8000`

**Terminal 2 - Frontend starten:**
```bash
cd frontend
npm run tauri dev
```

Die Desktop-App öffnet sich automatisch!

### Production Build

```bash
cd frontend
npm run tauri build
```

Die fertige App findest du in: `frontend/src-tauri/target/release/`

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

Backend API läuft auf: `http://127.0.0.1:8000`

### Endpoints

- `GET /api/health` - Health Check
- `GET /api/gpu/info` - GPU Informationen
- `POST /api/gpu/clear-cache` - GPU Cache leeren
- `GET /api/models` - Verfügbare Models auflisten
- `POST /api/models/load` - Model laden
- `POST /api/generate/image` - Bild generieren
- `GET /api/history` - Generation History
- `GET /api/stats` - Statistiken

API Docs: http://127.0.0.1:8000/docs (Swagger UI)

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

## 🙏 Credits

- Stable Diffusion by Stability AI
- Diffusers by HuggingFace
- Tauri Framework
- React & Tailwind CSS

---

**Viel Spaß beim Generieren! 🎨✨**
