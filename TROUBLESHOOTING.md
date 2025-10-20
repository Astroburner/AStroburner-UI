# 🔧 AI Studio - Troubleshooting Guide

Häufige Probleme und ihre Lösungen.

---

## 🐍 Backend Probleme

### Problem 1: `ModuleNotFoundError: No module named 'models'`

**Ursache:** Python findet die Module nicht (relative Import Probleme).

**Lösung:**
```bash
# Option 1: Starte Backend direkt aus dem backend Ordner
cd backend
venv\Scripts\activate
python main.py

# Option 2: Nutze das run.bat Script
cd backend
run.bat
```

**Die main.py wurde bereits gefixt mit:**
```python
import sys
from pathlib import Path
backend_dir = Path(__file__).parent
sys.path.insert(0, str(backend_dir))
```

### Problem 2: Virtual Environment nicht aktiviert

**Symptome:**
- `ModuleNotFoundError` für installierte Packages
- `torch` nicht gefunden

**Lösung:**
```bash
cd backend

# Windows:
venv\Scripts\activate

# Verify:
where python
# Sollte auf venv\Scripts\python.exe zeigen
```

### Problem 3: PyTorch nicht installiert

**Symptome:**
- `No module named 'torch'`
- `CUDA not available`

**Lösung:**
```bash
cd backend
venv\Scripts\activate

# RTX 5090 (CUDA 12.8):
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu128

# Verify:
python -c "import torch; print(torch.__version__); print(torch.cuda.is_available())"
```

### Problem 4: Port 8000 already in use

**Lösung:**
```bash
# Windows:
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Oder in config.py ändern:
API_PORT = 8001
```

---

## 🎨 Frontend Probleme

### Problem 1: Tauri Config Error - `Additional properties are not allowed`

**Fehlermeldung:**
```
Error `tauri.conf.json` error on `bundle`: Additional properties are not allowed ('identifier' was unexpected)
```

**Ursache:** Doppelte `identifier` Felder in tauri.conf.json (in v2 nicht erlaubt).

**Lösung:**
Die `tauri.conf.json` wurde bereits gefixt. `identifier` steht jetzt nur noch auf oberster Ebene, nicht mehr unter `bundle`.

**Alte (falsch):**
```json
{
  "identifier": "com.astroburner.ai-studio",
  "bundle": {
    "identifier": "com.astroburner.ai-studio"  // ❌ Doppelt!
  }
}
```

**Neu (korrekt):**
```json
{
  "identifier": "com.astroburner.ai-studio",
  "bundle": {
    // identifier entfernt ✅
  }
}
```

### Problem 2: `npm run tauri dev` schlägt fehl

**Ursache:** Dependencies nicht installiert oder Rust fehlt.

**Lösung:**
```bash
cd frontend

# Check Node Dependencies:
npm install

# Check Rust Installation:
rustc --version

# Falls Rust fehlt:
# https://rustup.rs/
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
```

### Problem 3: Rust Compilation dauert ewig

**Normal:** Beim ersten `npm run tauri dev` dauert die Rust Compilation 5-10 Minuten.

**Tipps:**
- Sei geduldig beim ersten Build
- Folgende Builds sind schneller (~30 Sekunden)
- Schließe andere Programme um RAM freizugeben

### Problem 4: Backend Connection Failed

**Symptome:**
- Frontend startet, aber zeigt keine Daten
- "Network Error" im Browser

**Lösung:**
```bash
# 1. Check ob Backend läuft:
curl http://127.0.0.1:8000/api/health

# 2. Falls nicht, starte Backend:
cd backend
venv\Scripts\activate
python main.py

# 3. Warte 5-10 Sekunden, dann Frontend neu starten
```

---

## 🚀 Tauri Spezifische Probleme

### Problem 1: Windows Defender blockiert App

**Lösung:**
```
Windows Security → Virus & threat protection → 
Manage settings → Add exclusion → Folder → 
Wähle: ai-studio\frontend\src-tauri\target\
```

### Problem 2: Visual Studio Build Tools fehlen (Windows)

**Fehlermeldung:**
```
error: linker `link.exe` not found
```

**Lösung:**
1. Download: https://visualstudio.microsoft.com/visual-cpp-build-tools/
2. Installiere "Desktop development with C++"
3. Neustart
4. Nochmal versuchen

### Problem 3: WebView2 fehlt (Windows)

**Lösung:**
- Windows 10/11: WebView2 ist normalerweise vorinstalliert
- Falls nicht: https://developer.microsoft.com/en-us/microsoft-edge/webview2/

---

## 💾 Database Probleme

### Problem 1: Database locked

**Lösung:**
```bash
# Stoppe alle Backend Instanzen
# Lösche Database Lock:
del ai_studio.db-wal
del ai_studio.db-shm

# Starte Backend neu
```

### Problem 2: Database file not found

**Normal:** Database wird automatisch beim ersten Start erstellt.

Falls Probleme:
```bash
cd backend
python -c "from models.database import Database; import asyncio; from config import settings; asyncio.run(Database(settings.DB_PATH).init_db())"
```

---

## 🎮 GPU / CUDA Probleme

### Problem 1: CUDA not available

**Check:**
```bash
python -c "import torch; print(f'CUDA: {torch.cuda.is_available()}'); print(f'GPU: {torch.cuda.get_device_name(0) if torch.cuda.is_available() else None}')"
```

**Lösungen:**

**a) NVIDIA Treiber veraltet:**
```
nvidia-smi
# Update auf neuesten Game Ready Driver
# https://www.nvidia.com/Download/index.aspx
```

**b) Falsche PyTorch Version:**
```bash
pip uninstall torch torchvision
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu128
```

**c) CUDA Toolkit fehlt:**
- Download: https://developer.nvidia.com/cuda-downloads
- Installiere CUDA 12.8 (RTX 5090)
- Neustart erforderlich

### Problem 2: Out of Memory (VRAM)

**RTX 5090 mit 32GB sollte das nie haben, aber falls doch:**

**Lösungen:**
```python
# In der App:
# - Kleinere Bildgröße (512x512 statt 1024x1024)
# - Weniger Steps (20-30 statt 50)
# - Settings → GPU Cache leeren

# Oder in backend/config.py:
DEFAULT_WIDTH = 512
DEFAULT_HEIGHT = 512
DEFAULT_STEPS = 30
```

### Problem 3: Slow Generation

**Check GPU Utilization:**
```bash
nvidia-smi -l 1
```

**Sollte zeigen:**
- GPU Util: 90-100%
- Power: Near max (575W für RTX 5090)
- Temp: 60-80°C

**Falls niedrig:**
```bash
# 1. Install xFormers für bessere Performance:
pip install xformers

# 2. Check Power Settings (Windows):
# Systemsteuerung → Energieoptionen → Höchstleistung

# 3. Verify CUDA Version Match:
python -c "import torch; print(torch.version.cuda)"
# Sollte "12.8" zeigen für RTX 5090
```

---

## 📦 Allgemeine Probleme

### Problem 1: start.bat öffnet und schließt sofort

**Lösung:**
```bash
# Starte manuell um Fehler zu sehen:

# Terminal 1 - Backend:
cd backend
run.bat

# Terminal 2 - Frontend:
cd frontend
run.bat
```

### Problem 2: Node.js oder Python nicht gefunden

**Check Installation:**
```bash
python --version  # Sollte 3.10+ sein
node --version    # Sollte 18+ sein
npm --version
```

**Falls fehlt:**
- Python: https://www.python.org/downloads/
- Node.js: https://nodejs.org/

### Problem 3: Git Bash vs CMD vs PowerShell

**Empfehlung für Windows:**
- Nutze **CMD** oder **PowerShell** für .bat Scripts
- Git Bash kann Probleme mit Windows Pfaden haben

---

## 🔍 Debug Tipps

### Backend Debug:
```bash
cd backend
venv\Scripts\activate

# Test Imports:
python -c "from api.routes import router"
python -c "from models.database import Database"
python -c "from core.model_manager import model_manager"

# Check Server:
python main.py
# Öffne Browser: http://127.0.0.1:8000/docs
```

### Frontend Debug:
```bash
# Browser Console öffnen (F12)
# Check für JavaScript Errors

# Network Tab:
# Check ob API Calls funktionieren
# Sollte sehen: http://127.0.0.1:8000/api/...
```

### GPU Debug:
```bash
# NVIDIA Info:
nvidia-smi

# PyTorch CUDA Test:
python -c "import torch; print(torch.cuda.get_device_properties(0))"

# Backend GPU Monitor Test:
cd backend
venv\Scripts\activate
python -c "from core.gpu_monitor import gpu_monitor; print(gpu_monitor.get_gpu_info())"
```

---

## 📞 Weitere Hilfe

Wenn nichts funktioniert:

1. **Check Logs:**
   - Backend: Terminal Output
   - Frontend: Browser Console (F12)

2. **Copy Error Messages:**
   - Komplette Fehlermeldung
   - Stack Trace
   - System Info (Windows Version, GPU, Python Version)

3. **Erstelle GitHub Issue** mit:
   - Fehlermeldung
   - Was du versucht hast
   - System Info

---

## ✅ Quick Fix Checkliste

Bevor du um Hilfe fragst, check:

- [ ] Virtual Environment aktiviert?
- [ ] PyTorch installiert mit richtiger CUDA Version?
- [ ] Backend läuft? (curl http://127.0.0.1:8000/api/health)
- [ ] Node modules installiert? (frontend/node_modules exists)
- [ ] Rust installiert? (rustc --version)
- [ ] NVIDIA Treiber aktuell? (nvidia-smi)
- [ ] Port 8000 frei? (netstat -ano | findstr :8000)

---

**Die meisten Probleme sind schnell gelöst! Bei Fragen melde dich! 🚀**
