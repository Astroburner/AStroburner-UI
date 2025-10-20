# GPU/CUDA Problem diagnostizieren

## Problem: "No GPU" angezeigt, CUDA: False

Das bedeutet PyTorch wurde **ohne CUDA Support** installiert (CPU-Version).

## Diagnose-Schritte

### 1. Prüfe ob NVIDIA Treiber funktionieren

**In CMD/PowerShell:**
```cmd
nvidia-smi
```

**Sollte zeigen:**
```
+-------------------------------------------------------------------------+
| NVIDIA-SMI 566.xx       Driver Version: 566.xx       CUDA Version: 12.8|
|-------------------------------------------------------------------------+
| GPU  Name                    TCC/WDDM | Bus-Id        Disp.A | Volatile|
|   0  NVIDIA GeForce RTX 5090   WDDM  | 00000000:01:00.0 Off |    Off  |
|-------------------------------------------------------------------------+
```

✅ **Wenn RTX 5090 erscheint:** Treiber OK, PyTorch Problem
❌ **Wenn Fehler:** Treiber neu installieren

---

### 2. Prüfe PyTorch CUDA Version

**Im Backend-Ordner:**
```cmd
cd C:\KI_Weltherschaft\Astroburner_UI\V1_2\ai-studio\backend
venv\Scripts\activate
python -c "import torch; print(f'PyTorch: {torch.__version__}'); print(f'CUDA available: {torch.cuda.is_available()}'); print(f'CUDA version: {torch.version.cuda}')"
```

**Mögliche Ausgaben:**

**A) CUDA ist False:**
```
PyTorch: 2.5.1+cpu
CUDA available: False
CUDA version: None
```
→ **CPU-Version installiert** (FALSCH!)

**B) CUDA ist True:**
```
PyTorch: 2.5.1+cu128
CUDA available: True
CUDA version: 12.8
```
→ **CUDA-Version installiert** (RICHTIG!)

---

## Lösung: PyTorch mit CUDA neu installieren

### Schritt 1: Alte PyTorch-Version deinstallieren

```cmd
cd C:\KI_Weltherschaft\Astroburner_UI\V1_2\ai-studio\backend
venv\Scripts\activate

pip uninstall torch torchvision torchaudio -y
```

### Schritt 2: PyTorch mit CUDA 12.8 installieren

**Für RTX 5090 (CUDA 12.8):**
```cmd
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu128
```

**WICHTIG:** Das `--index-url` ist entscheidend!

**Download-Größe:** ~2-3 GB
**Dauer:** 3-5 Minuten

### Schritt 3: Verifizierung

```cmd
python -c "import torch; print(f'PyTorch: {torch.__version__}'); print(f'CUDA available: {torch.cuda.is_available()}'); print(f'CUDA version: {torch.version.cuda}'); print(f'GPU Name: {torch.cuda.get_device_name(0) if torch.cuda.is_available() else \"N/A\"}')"
```

**Sollte zeigen:**
```
PyTorch: 2.5.1+cu128
CUDA available: True
CUDA version: 12.8
GPU Name: NVIDIA GeForce RTX 5090
```

✅ **CUDA ist jetzt aktiviert!**

---

### Schritt 4: Backend neu starten

```cmd
# Im Backend Terminal: CTRL+C drücken
python main.py
```

**Backend sollte zeigen:**
```
INFO: Starting AI Studio v1.2.0
INFO: Database initialized
Device: CUDA (cuda:0)
GPU: NVIDIA GeForce RTX 5090
VRAM: 32 GB
```

### Schritt 5: Frontend aktualisieren

**Frontend läuft bereits?**
- Einfach Seite neu laden (F5)
- Header sollte jetzt RTX 5090 zeigen

---

## Häufige Probleme

### Problem 1: "CUDA not found" Fehler

**Symptom:**
```
RuntimeError: Couldn't load custom C++ ops. 
This can happen if your PyTorch and torchvision versions are incompatible
```

**Lösung:**
```cmd
pip uninstall torch torchvision -y
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu128 --force-reinstall
```

---

### Problem 2: "CUDA driver version insufficient"

**Symptom:**
```
NVIDIA driver on your system is too old (found version xxxx)
```

**Lösung:**
1. Besuche: https://www.nvidia.com/download/index.aspx
2. Wähle: RTX 50 Series → RTX 5090
3. Lade neuesten Treiber herunter (566.xx+)
4. Installiere und starte PC neu

---

### Problem 3: PyTorch installiert CPU statt CUDA

**Ursache:** `--index-url` wurde vergessen

**FALSCH:**
```cmd
pip install torch torchvision
# → Installiert CPU-Version!
```

**RICHTIG:**
```cmd
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu128
# → Installiert CUDA 12.8 Version!
```

---

### Problem 4: "Multiple CUDA versions" Konflikt

**Symptom:**
```
Found CUDA 11.8 and CUDA 12.8 installed
```

**Lösung:**
```cmd
# PyTorch nutzt die richtige Version wenn korrekt installiert
pip uninstall torch torchvision -y
pip cache purge
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu128
```

---

## Automatischer Fix-Script

**Erstelle:** `backend/fix_cuda.bat`

```batch
@echo off
echo ========================================
echo    AI Studio - CUDA Fix Script
echo ========================================
echo.
echo This will reinstall PyTorch with CUDA 12.8 support
echo for RTX 5090 / RTX 50-series GPUs
echo.
pause

cd /d "%~dp0"

echo [1/4] Activating virtual environment...
call venv\Scripts\activate
if %errorlevel% neq 0 (
    echo ERROR: Failed to activate venv!
    pause
    exit /b 1
)

echo [2/4] Uninstalling old PyTorch...
pip uninstall torch torchvision torchaudio -y

echo [3/4] Installing PyTorch with CUDA 12.8...
echo This will download ~2-3 GB...
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu128

if %errorlevel% neq 0 (
    echo ERROR: Failed to install PyTorch!
    pause
    exit /b 1
)

echo [4/4] Verifying installation...
python -c "import torch; print(f'\nPyTorch: {torch.__version__}'); print(f'CUDA available: {torch.cuda.is_available()}'); print(f'CUDA version: {torch.version.cuda}'); print(f'GPU: {torch.cuda.get_device_name(0) if torch.cuda.is_available() else \"N/A\"}'); print(f'GPU Count: {torch.cuda.device_count()}')"

echo.
echo ========================================
echo    Installation Complete!
echo ========================================
echo.
echo Next steps:
echo 1. Restart backend: python main.py
echo 2. Reload frontend UI (F5)
echo 3. Check GPU info in header
echo.
pause
```

**Ausführen:**
```cmd
cd backend
fix_cuda.bat
```

---

## Weitere GPU-Checks

### Check 1: CUDA Toolkit Version

```cmd
nvcc --version
```

**Nicht installiert?** Ist OK! PyTorch bringt eigenes CUDA mit.

### Check 2: cuDNN Status

```cmd
python -c "import torch; print(torch.backends.cudnn.enabled)"
```

**Sollte:** `True`

### Check 3: GPU Compute Capability

```cmd
python -c "import torch; print(f'Compute Capability: {torch.cuda.get_device_capability(0)}')"
```

**RTX 5090 sollte zeigen:** `(8, 9)` oder `(9, 0)`

---

## Nach erfolgreichem Fix

**UI Header sollte zeigen:**
```
GPU: RTX 5090 | VRAM: 2.1 / 32.0 GB | 45°C | 15% Util
```

**Backend Terminal:**
```
INFO: Starting AI Studio v1.2.0
Device: CUDA (cuda:0)
GPU: NVIDIA GeForce RTX 5090
Memory: 32.0 GB
Compute Capability: 8.9
```

**Erste Generierung:**
- SDXL 1024x1024: ~4-6 Sekunden (statt Minuten auf CPU!)
- GPU Nutzung: 95-100%
- VRAM Usage: ~8-10 GB

---

## Zusammenfassung - Quick Fix

```cmd
# 1. Backend aktivieren
cd C:\KI_Weltherschaft\Astroburner_UI\V1_2\ai-studio\backend
venv\Scripts\activate

# 2. PyTorch neu installieren
pip uninstall torch torchvision -y
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu128

# 3. Verifizieren
python -c "import torch; print(torch.cuda.is_available())"
# Sollte: True

# 4. Backend neu starten
python main.py

# 5. Frontend neu laden (F5)
```

**Fertig! RTX 5090 sollte jetzt funktionieren! 🚀**
