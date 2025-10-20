# 🚀 AI Studio - Detaillierte Setup Anleitung

## Inhaltsverzeichnis
1. [System Requirements](#system-requirements)
2. [Python Setup](#python-setup)
3. [Node.js Setup](#nodejs-setup)
4. [Rust Setup](#rust-setup)
5. [GPU Setup (NVIDIA)](#gpu-setup-nvidia)
6. [Apple Silicon Setup](#apple-silicon-setup)
7. [Erste Schritte](#erste-schritte)
8. [Bekannte Probleme](#bekannte-probleme)

---

## System Requirements

### Minimum
- **OS:** Windows 10 (64-bit), macOS 11+, Ubuntu 20.04+
- **RAM:** 16GB
- **GPU:** NVIDIA GPU mit 6GB+ VRAM (oder Apple Silicon)
- **Speicher:** 30GB frei (für Models und Dependencies)

### Empfohlen
- **RAM:** 32GB+
- **GPU:** NVIDIA RTX 3060/4060 oder besser (12GB+ VRAM)
- **Speicher:** 50GB+ SSD

---

## Python Setup

### 1. Python Installation

#### Windows
```powershell
# Download Python 3.10 von python.org
# https://www.python.org/downloads/

# Bei Installation: "Add Python to PATH" aktivieren!

# Verify:
python --version
# Output: Python 3.10.x oder 3.11.x
```

#### macOS
```bash
# Mit Homebrew:
brew install python@3.10

# Verify:
python3 --version
```

#### Linux (Ubuntu)
```bash
sudo apt update
sudo apt install python3.10 python3.10-venv python3-pip
```

### 2. Virtual Environment Setup

```bash
cd ai-studio/backend

# Virtual Environment erstellen
python -m venv venv

# Aktivieren:
# Windows (PowerShell):
.\venv\Scripts\Activate.ps1

# Windows (CMD):
venv\Scripts\activate.bat

# macOS/Linux:
source venv/bin/activate

# Verify (sollte (venv) im Prompt zeigen):
which python  # sollte auf venv/bin/python zeigen
```

### 3. PyTorch Installation

#### NVIDIA GPU (CUDA 12.1)
```bash
pip install torch==2.5.1 torchvision==0.20.1 --index-url https://download.pytorch.org/whl/cu121
```

#### Apple Silicon (MPS)
```bash
pip install torch==2.5.1 torchvision==0.20.1
```

#### CPU Only (Fallback)
```bash
pip install torch==2.5.1 torchvision==0.20.1 --index-url https://download.pytorch.org/whl/cpu
```

### 4. Backend Dependencies
```bash
pip install -r requirements.txt
```

### 5. Test Installation
```bash
python -c "import torch; print(f'PyTorch: {torch.__version__}'); print(f'CUDA Available: {torch.cuda.is_available()}'); print(f'CUDA Device: {torch.cuda.get_device_name(0) if torch.cuda.is_available() else None}')"
```

---

## Node.js Setup

### 1. Node.js Installation

#### Windows
```powershell
# Download von nodejs.org (LTS Version)
# https://nodejs.org/

# Verify:
node --version  # v18.x oder höher
npm --version   # v9.x oder höher
```

#### macOS
```bash
# Mit Homebrew:
brew install node@18

# Verify:
node --version
npm --version
```

#### Linux (Ubuntu)
```bash
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt install -y nodejs
```

### 2. Frontend Dependencies
```bash
cd ai-studio/frontend
npm install
```

---

## Rust Setup

Tauri benötigt Rust für die Desktop-App.

### 1. Rust Installation

#### Windows / macOS / Linux
```bash
# Download und Installation:
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh

# Nach Installation: Terminal neu starten

# Verify:
rustc --version
cargo --version
```

### 2. System Dependencies

#### Windows
- **Microsoft C++ Build Tools:**
  - Download: https://visualstudio.microsoft.com/visual-cpp-build-tools/
  - Installiere "Desktop development with C++"

#### macOS
```bash
# Xcode Command Line Tools:
xcode-select --install
```

#### Linux (Ubuntu/Debian)
```bash
sudo apt update
sudo apt install -y \
    libwebkit2gtk-4.0-dev \
    build-essential \
    curl \
    wget \
    file \
    libssl-dev \
    libgtk-3-dev \
    libayatana-appindicator3-dev \
    librsvg2-dev
```

---

## GPU Setup (NVIDIA)

### 1. CUDA Toolkit Installation

#### Windows
1. Download CUDA Toolkit 12.1:
   https://developer.nvidia.com/cuda-downloads
2. Installiere mit Standard-Einstellungen
3. Neustart erforderlich

#### Linux (Ubuntu)
```bash
# CUDA 12.1
wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2204/x86_64/cuda-keyring_1.1-1_all.deb
sudo dpkg -i cuda-keyring_1.1-1_all.deb
sudo apt update
sudo apt install cuda-12-1
```

### 2. cuDNN Installation (Optional für bessere Performance)

1. Download cuDNN von NVIDIA (benötigt Account):
   https://developer.nvidia.com/cudnn
2. Extrahiere und kopiere Files in CUDA Verzeichnis

### 3. Verify CUDA
```bash
nvidia-smi
# Sollte GPU Info anzeigen

nvcc --version
# Sollte CUDA Version anzeigen
```

---

## Apple Silicon Setup

Für M1/M2/M3 Macs:

```bash
# PyTorch mit MPS Support ist bereits in requirements.txt

# Test MPS:
python -c "import torch; print(f'MPS Available: {torch.backends.mps.is_available()}')"
# Sollte "True" ausgeben
```

---

## Erste Schritte

### 1. Backend Starten

```bash
cd ai-studio/backend

# Virtual Environment aktivieren
source venv/bin/activate  # oder venv\Scripts\activate

# Server starten
python main.py
```

**Erwartete Output:**
```
INFO:     Started server process
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete.
```

### 2. Frontend Starten (neues Terminal)

```bash
cd ai-studio/frontend

# Development Mode:
npm run tauri dev
```

**Erwartete Output:**
- Vite Dev Server startet auf Port 3000
- Tauri kompiliert Rust Code (kann beim ersten Mal 5-10 Min dauern)
- Desktop App öffnet sich automatisch

### 3. Erstes Model Laden

1. App öffnet sich
2. Klicke auf "Settings" Tab
3. Unter "Models" → "SDXL Turbo" → "Laden"
4. Warte bis Model heruntergeladen ist (~6.9GB)
5. Gehe zu "Generate" Tab
6. Generiere dein erstes Bild!

---

## Bekannte Probleme

### Problem: "ModuleNotFoundError: No module named 'torch'"

**Lösung:**
```bash
# Virtual Environment aktivieren!
cd backend
source venv/bin/activate  # oder venv\Scripts\activate
pip install -r requirements.txt
```

### Problem: CUDA Out of Memory

**Lösung:**
```bash
# In backend/config.py:
DEFAULT_WIDTH = 512  # Statt 1024
DEFAULT_HEIGHT = 512

# Oder in der App:
# - Kleinere Bilder generieren (512x512)
# - Weniger Steps (20-30)
# - GPU Cache leeren (Settings → GPU)
```

### Problem: Models werden nicht gefunden

**Lösung:**
```bash
# Models werden automatisch in "models/" Ordner heruntergeladen
# Bei Problemen: Ordner manuell erstellen
mkdir -p models
```

### Problem: Tauri Build fails

**Lösung:**
```bash
# Windows: Installiere Visual Studio Build Tools
# macOS: xcode-select --install
# Linux: sudo apt install build-essential

# Rust neu installieren:
rustup update
```

### Problem: Port 8000 already in use

**Lösung:**
```bash
# Backend config.py ändern:
API_PORT = 8001  # oder anderen freien Port

# Oder bestehenden Prozess beenden:
# Windows:
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# macOS/Linux:
lsof -ti:8000 | xargs kill -9
```

---

## Performance Optimierungen

### 1. xFormers (NVIDIA Only)

```bash
pip install xformers
```

Spart ~30% VRAM!

### 2. Model Caching

Models werden in `models/` gecacht. Nicht löschen!

### 3. GPU Settings

In `backend/config.py`:
```python
ENABLE_XFORMERS = True
ENABLE_ATTENTION_SLICING = True
VAE_SLICING = True
```

---

## Support

Bei Problemen:
1. Check Console Output (Backend Terminal)
2. Check Browser Console (F12 in App)
3. Erstelle GitHub Issue mit Error Logs

---

**Happy Generating! 🎨**
