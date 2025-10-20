# 📥 AI Studio - Download & Installation

## 🎉 Projekt ist fertig und bereit zum Download!

---

## 📦 Download

### Option 1: Direct Download (Empfohlen)

**Backup Download Link:**
```
https://page.gensparksite.com/project_backups/ai-studio-v1.0.0.tar.gz
```

**Größe:** ~93 KB (komprimiert, enthält kompletten Source Code)

### Option 2: Von dieser Sandbox

Falls du direkten Zugriff auf diese Sandbox hast:
```bash
# Komplettes Projekt liegt in:
/home/user/ai-studio/
```

---

## 🚀 Installation auf deinem PC

### 1. Datei extrahieren

**Windows:**
```powershell
# Mit 7-Zip oder WinRAR extrahieren
# Oder mit tar (in PowerShell):
tar -xzf ai-studio-v1.0.0.tar.gz
cd ai-studio
```

**macOS/Linux:**
```bash
tar -xzf ai-studio-v1.0.0.tar.gz
cd ai-studio
```

### 2. Voraussetzungen installieren

#### Python 3.10+
- **Windows:** https://www.python.org/downloads/
- **macOS:** `brew install python@3.10`
- **Linux:** `sudo apt install python3.10 python3.10-venv`

#### Node.js 18+
- **Alle Plattformen:** https://nodejs.org/ (LTS Version)

#### Rust (für Tauri)
```bash
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
```

#### CUDA (optional, für NVIDIA GPU)
- Download: https://developer.nvidia.com/cuda-downloads
- Wähle CUDA 12.1

### 3. Backend Setup

```bash
cd backend

# Virtual Environment erstellen
python -m venv venv

# Aktivieren
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Dependencies installieren
pip install -r requirements.txt

# PyTorch Installation - Wähle basierend auf deiner GPU:

# RTX 5090 / RTX 50-series (CUDA 12.8):
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu128

# RTX 4090 / RTX 40-series (CUDA 12.1):
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu121

# RTX 3090 / RTX 30-series (CUDA 11.8):
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118

# Apple Silicon (M1/M2/M3):
pip install torch torchvision

# CPU only (langsam):
pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu
```

### 4. Frontend Setup

```bash
cd ../frontend

# Node Dependencies
npm install

# Das war's! ✨
```

### 5. App Starten

**Option A: Automatisch (Empfohlen)**

```bash
# Windows:
start.bat

# macOS/Linux:
./start.sh
```

**Option B: Manuell**

Terminal 1 - Backend:
```bash
cd backend
source venv/bin/activate  # Windows: venv\Scripts\activate
python main.py
```

Terminal 2 - Frontend:
```bash
cd frontend
npm run tauri dev
```

### 6. Erste Generierung! 🎨

1. App startet automatisch (kann beim ersten Mal 5-10 Min dauern wegen Rust Compilation)
2. **Settings** → **Models** → **"SDXL Turbo"** → **Laden** (wartet bis Download fertig)
3. **Generate** → Prompt eingeben: `"a beautiful sunset over mountains"`
4. **Parameter:** Width: 512, Height: 512, Steps: 4
5. **"Bild Generieren"** klicken
6. Fertig! 🎉

---

## 📚 Enthaltene Dokumentation

- **README.md** - Hauptdokumentation mit allen Features
- **SETUP.md** - Detaillierte Setup-Anleitung für alle Plattformen
- **QUICKSTART.md** - 5-Minuten Quick Start Guide
- **CONTRIBUTING.md** - Guide für Entwickler
- **PROJECT_SUMMARY.md** - Vollständige Projektübersicht
- **LICENSE** - MIT License

---

## 📊 Was ist enthalten?

### Backend (Python)
- ✅ FastAPI Server
- ✅ PyTorch + Diffusers Integration
- ✅ Model Manager (SD1.5, SDXL, SDXL-Turbo)
- ✅ GPU Monitoring
- ✅ SQLite Database
- ✅ REST API

### Frontend (React + Tauri)
- ✅ Modern Dark UI
- ✅ Generation Panel
- ✅ Image Gallery
- ✅ History & Search
- ✅ Settings Panel
- ✅ GPU Monitoring Display

### Desktop
- ✅ Tauri 2.0 Configuration
- ✅ Cross-Platform Build Setup
- ✅ Rust Backend

### Extras
- ✅ Startup Scripts (Windows + macOS/Linux)
- ✅ Git Repository
- ✅ Comprehensive Documentation
- ✅ Example Environment Variables

---

## 🔧 System Requirements

### Minimum
- **OS:** Windows 10, macOS 11+, Ubuntu 20.04+
- **RAM:** 16GB
- **GPU:** NVIDIA mit 6GB VRAM (oder Apple Silicon)
- **Storage:** 30GB frei

### Empfohlen
- **RAM:** 32GB
- **GPU:** NVIDIA RTX 3060/4060 (12GB VRAM)
- **Storage:** 50GB SSD

---

## 🐛 Troubleshooting

### Problem: Python nicht gefunden
```bash
python --version
# Falls nicht gefunden: Python installieren und zu PATH hinzufügen
```

### Problem: npm nicht gefunden
```bash
node --version
npm --version
# Falls nicht gefunden: Node.js installieren
```

### Problem: CUDA nicht gefunden
```bash
nvidia-smi
# Falls nicht gefunden: NVIDIA Treiber + CUDA Toolkit installieren
```

### Problem: Backend startet nicht
```bash
# Virtual Environment aktivieren!
cd backend
source venv/bin/activate  # Windows: venv\Scripts\activate
python main.py
```

### Problem: Frontend baut nicht
```bash
# Rust installieren
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
# Terminal neu starten
cd frontend
npm install
npm run tauri dev
```

---

## 📞 Support

Bei Problemen:

1. **Check Logs:**
   - Backend: Terminal Output
   - Frontend: Browser Console (F12)

2. **Lese Dokumentation:**
   - [README.md](README.md)
   - [SETUP.md](SETUP.md)
   - [QUICKSTART.md](QUICKSTART.md)

3. **GitHub Issues:**
   - Erstelle ein Issue mit Error Logs

---

## 🎯 Quick Start Zusammenfassung

```bash
# 1. Download & Extract
tar -xzf ai-studio-v1.0.0.tar.gz
cd ai-studio

# 2. Backend Setup
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
# Wähle deine CUDA Version:
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu128  # RTX 5090
# pip install torch torchvision --index-url https://download.pytorch.org/whl/cu121  # RTX 4090
# pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118  # RTX 3090

# 3. Frontend Setup
cd ../frontend
npm install

# 4. Starten
cd ..
./start.sh  # oder start.bat auf Windows

# 5. In der App: Settings → Load Model → Generate!
```

---

## ✨ Features Highlights

- 🎨 **Text-to-Image Generation** mit mehreren Models
- ⚡ **GPU Acceleration** mit CUDA/MPS
- 🖼️ **Beautiful Gallery** mit Fullscreen & Download
- 📊 **Real-time GPU Monitoring**
- 💾 **History System** mit Suche
- 🎛️ **Vollständige Parameter-Kontrolle**
- 🌙 **Modern Dark UI**
- 🔒 **Secure Desktop App** mit Tauri

---

## 🎉 Viel Erfolg!

Die App ist komplett fertig und bereit für den produktiven Einsatz!

Bei Fragen oder Feedback melde dich gerne! 🚀

---

**Version:** 1.0.0  
**Build:** 2025-10-20  
**Autor:** Astroburner
