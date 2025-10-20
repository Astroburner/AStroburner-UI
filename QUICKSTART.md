# ⚡ AI Studio - Quick Start Guide

Schnellstart in 5 Minuten! 🚀

## Voraussetzungen Check

✅ **Python 3.10+** installiert?
```bash
python --version
```

✅ **Node.js 18+** installiert?
```bash
node --version
```

✅ **Git** installiert?
```bash
git --version
```

✅ **NVIDIA GPU** (optional, aber empfohlen)?
```bash
nvidia-smi
```

Wenn etwas fehlt → Siehe [SETUP.md](SETUP.md)

---

## 🚀 Installation (5 Minuten)

### 1. Repository Klonen
```bash
git clone https://github.com/yourusername/ai-studio.git
cd ai-studio
```

### 2. Backend Setup
```bash
cd backend

# Virtual Environment
python -m venv venv

# Aktivieren
source venv/bin/activate  # macOS/Linux
# ODER
venv\Scripts\activate     # Windows

# Dependencies installieren
pip install -r requirements.txt

# PyTorch mit CUDA (NVIDIA GPU):
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu121

# PyTorch CPU only (ohne GPU):
# pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu
```

### 3. Frontend Setup
```bash
cd ../frontend
npm install
```

---

## 🎮 Starten

### Option A: Automatischer Start (empfohlen)

**macOS/Linux:**
```bash
./start.sh
```

**Windows:**
```bash
start.bat
```

### Option B: Manueller Start

**Terminal 1 - Backend:**
```bash
cd backend
source venv/bin/activate  # oder venv\Scripts\activate
python main.py
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run tauri dev
```

---

## 🎨 Erste Generierung

1. **App startet automatisch** (kann beim ersten Mal 5-10 Min dauern)

2. **Model laden:**
   - Klicke "Settings" Tab
   - "Models" → "SDXL Turbo" → "Laden"
   - Warte bis Download fertig (~6.9GB)

3. **Bild generieren:**
   - Zurück zu "Generate" Tab
   - Prompt eingeben: "a beautiful sunset over mountains, photorealistic"
   - Parameter (für schnelles Testen):
     - Width: 512
     - Height: 512
     - Steps: 4
     - Guidance: 1.0
   - Klick "Bild Generieren"

4. **Fertig!** 🎉

---

## 📊 Parameter Empfehlungen

### Schnelle Generierung (5-10 Sekunden)
```
Model: SDXL Turbo
Size: 512x512
Steps: 4-8
Guidance: 0-1
```

### Gute Qualität (20-30 Sekunden)
```
Model: SDXL Base
Size: 768x768
Steps: 25-35
Guidance: 7-8
```

### Beste Qualität (45+ Sekunden)
```
Model: SDXL Base
Size: 1024x1024
Steps: 40-50
Guidance: 7-9
```

---

## 🐛 Häufige Probleme

### Backend startet nicht
```bash
# Virtual Environment vergessen?
cd backend
source venv/bin/activate
python main.py
```

### Frontend baut nicht
```bash
# Rust fehlt?
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
```

### CUDA nicht gefunden
```bash
# CUDA installiert?
nvidia-smi

# PyTorch neu installieren:
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu121
```

### Out of Memory (VRAM)
- Kleinere Bildgröße: 512x512
- Weniger Steps: 20-30
- Settings → GPU Cache leeren

---

## 📚 Weiterführende Docs

- [Vollständiges README](README.md)
- [Detaillierte Setup Anleitung](SETUP.md)
- [Contributing Guide](CONTRIBUTING.md)

---

## 🎯 Nächste Schritte

1. ✅ Experimentiere mit verschiedenen Prompts
2. ✅ Probiere verschiedene Models aus
3. ✅ Check History Tab für deine Generationen
4. ✅ Optimiere Parameter für deine GPU
5. ✅ Erstelle coole Kunstwerke! 🎨

---

## 💡 Prompt Tips

**Gute Prompts:**
```
"a majestic lion in savanna, golden hour lighting, photorealistic, 4k"
"cyberpunk city at night, neon lights, rain, cinematic"
"oil painting of a medieval castle, dramatic clouds"
```

**Negative Prompts (was vermeiden):**
```
"blurry, low quality, distorted, ugly, bad anatomy"
```

---

**Viel Erfolg! Bei Fragen → GitHub Issues 🚀**
