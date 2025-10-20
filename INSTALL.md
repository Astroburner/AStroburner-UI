# AI Studio - Complete Installation Guide

Version: 1.6.0

## 📋 Voraussetzungen

### System Requirements
- **OS:** Windows 10/11, macOS 12+, or Linux (Ubuntu 20.04+)
- **RAM:** 16GB minimum, 32GB+ recommended
- **Storage:** 20GB+ free space for models
- **GPU:** NVIDIA GPU mit 8GB+ VRAM (empfohlen für RTX 5090)

### Software Requirements
- **Python:** 3.10, 3.11, or 3.12
- **Node.js:** 18+ or 20+
- **npm:** 10+
- **Rust:** Latest stable (für Tauri)
- **Visual Studio Build Tools** (Windows only)

---

## 🚀 Option 1: Automatische Installation (EMPFOHLEN)

### Windows:
```bash
# 1. Entpacke das Projekt
# 2. Navigiere ins Verzeichnis
cd C:\Pfad\zu\ai-studio

# 3. Führe Setup aus
setup.bat
```

Das Setup-Script:
- ✅ Prüft alle System-Anforderungen
- ✅ Erstellt Python Virtual Environment
- ✅ Installiert Backend Dependencies (PyTorch + alle anderen)
- ✅ Installiert Frontend Dependencies (inkl. Dialog Plugin)
- ✅ Zeigt interaktives Menü nach Installation

**Nach dem Setup:**
```bash
start.bat  # Startet Backend + Frontend automatisch
```

---

## 🔧 Option 2: Manuelle Installation

### Schritt 1: Backend Installation

#### 1.1 Python Virtual Environment erstellen
```bash
cd backend
python -m venv venv
```

#### 1.2 Virtual Environment aktivieren
**Windows:**
```bash
venv\Scripts\activate
```

**macOS/Linux:**
```bash
source venv/bin/activate
```

#### 1.3 PyTorch installieren (GPU-spezifisch)

**CUDA 12.8 (RTX 5090, RTX 50-series):**
```bash
pip install -r requirements-cuda128.txt
```

**CUDA 12.1 (RTX 4090, RTX 40-series):**
```bash
pip install -r requirements-cuda121.txt
```

**CPU only:**
```bash
pip install torch==2.5.1 torchvision==0.20.1 --index-url https://download.pytorch.org/whl/cpu
pip install -r requirements.txt
```

**Apple Silicon (M1/M2/M3):**
```bash
pip install torch==2.5.1 torchvision==0.20.1
pip install -r requirements.txt
```

#### 1.4 Alle Backend Dependencies installieren
```bash
pip install -r requirements.txt
```

### Schritt 2: Frontend Installation

```bash
cd ../frontend
npm install
```

**Wichtig:** Das Dialog Plugin (`@tauri-apps/plugin-dialog`) ist bereits in `package.json` enthalten und wird automatisch installiert.

### Schritt 3: Rust & Build Tools (falls noch nicht vorhanden)

**Rust installieren:**
- Windows/macOS/Linux: https://rustup.rs/

**Visual Studio Build Tools (nur Windows):**
- Download: https://visualstudio.microsoft.com/downloads/#build-tools-for-visual-studio-2022
- Installiere "Desktop development with C++"

---

## ✅ Installation Überprüfen

### Backend Test:
```bash
cd backend
venv\Scripts\activate  # Windows
source venv/bin/activate  # macOS/Linux
python -c "import torch; print(f'PyTorch: {torch.__version__}'); print(f'CUDA: {torch.cuda.is_available()}')"
```

**Erwartete Ausgabe:**
```
PyTorch: 2.5.1
CUDA: True  # (wenn GPU vorhanden)
```

### Frontend Test:
```bash
cd frontend
npm run dev
```

Browser sollte sich öffnen auf `http://localhost:3000`

---

## 📦 Requirements Files Übersicht

### Haupt-Requirements:
- **`requirements.txt`** - Alle Backend Dependencies (mit PyTorch >= 2.5.0)
- **`requirements-dev.txt`** - Development Tools (pytest, black, mypy, etc.)

### GPU-spezifische Requirements:
- **`requirements-cuda128.txt`** - RTX 5090, RTX 50-series (CUDA 12.8)
- **`requirements-cuda121.txt`** - RTX 4090, RTX 40-series (CUDA 12.1)

### Beispiel - RTX 5090:
```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements-cuda128.txt  # Installiert alles mit CUDA 12.8
```

---

## 🐛 Troubleshooting

### Problem: "torch not found" oder CUDA nicht verfügbar

**Lösung:**
```bash
# Deinstalliere alte PyTorch Version
pip uninstall torch torchvision

# Installiere korrekte Version für deine GPU
# Für RTX 5090:
pip install torch==2.5.1 torchvision==0.20.1 --index-url https://download.pytorch.org/whl/cu128
```

### Problem: "Failed to resolve import @tauri-apps/plugin-dialog"

**Lösung:**
```bash
cd frontend
npm install  # Dialog Plugin ist bereits in package.json
```

Oder verwende Quick-Fix:
```bash
quick-fix-dependencies.bat
```

### Problem: Pydantic Warning "model_type conflicts with protected namespace"

**Status:** ✅ Bereits gefixt in v1.6.0
- Die Warning ist harmlos und wurde behoben

### Problem: "Rust not found" bei Frontend Build

**Lösung:**
```bash
# Installiere Rust
# Windows: Lade Installer von https://rustup.rs/
# macOS/Linux: curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh

# Nach Installation, Terminal neu öffnen und verifizieren:
rustc --version
cargo --version
```

---

## 🎯 Nach der Installation

### App starten:
```bash
# Option 1: Automatisch (Backend + Frontend)
start.bat

# Option 2: Manuell
# Terminal 1 - Backend:
cd backend
venv\Scripts\activate
python main.py

# Terminal 2 - Frontend:
cd frontend
npm run tauri dev
```

### Erste Schritte:
1. ✅ Settings → Models → Model laden (z.B. SDXL-Turbo)
2. ✅ Generate Panel → Prompt eingeben → Bild generieren
3. ✅ Settings → LoRAs → LoRA hinzufügen (optional)
4. ✅ History Panel → Generierte Bilder anschauen

---

## 📚 Weitere Dokumentation

- **QUICKSTART.md** - Schnellstart-Anleitung
- **TROUBLESHOOTING.md** - Häufige Probleme & Lösungen
- **RTX_5090_SETUP.md** - GPU-spezifische Optimierungen
- **CHANGELOG.md** - Version History & Features

---

Bei Problemen siehe auch: **TROUBLESHOOTING.md** oder erstelle ein Issue auf GitHub.
