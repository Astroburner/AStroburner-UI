# 🚀 setup.bat - Automatische Installation für Windows

## Was macht setup.bat?

Das **setup.bat** Script automatisiert die **komplette Installation** von AI Studio auf Windows!

---

## ✨ Features

### Automatische Checks:
- ✅ Python Installation & Version
- ✅ Node.js Installation & Version  
- ✅ npm Verfügbarkeit
- ✅ Git Installation (optional)
- ✅ NVIDIA GPU Erkennung
- ✅ Rust Installation (Tauri)
- ✅ Visual Studio Build Tools

### Automatische Installation:
- ✅ Python Virtual Environment
- ✅ Python Dependencies (FastAPI, etc.)
- ✅ PyTorch mit **automatischer CUDA Version Erkennung**
- ✅ Node.js Dependencies (React, Tauri)
- ✅ Komplette Verifikation

### Interaktiv:
- 🎯 Wähle deine GPU-Generation (RTX 50/40/30-series)
- 🎯 Automatische PyTorch Installation für deine Hardware
- 🎯 Hilfreiche Links falls etwas fehlt
- 🎯 Klare Fortschrittsanzeigen

---

## 🎮 Verwendung

### Schnellstart:

```cmd
# 1. Öffne Terminal im ai-studio Ordner
cd C:\KI_Weltherschaft\Astroburner_UI\ai-studio

# 2. Starte Setup
setup.bat

# 3. Folge den Anweisungen
```

Das war's! Der Rest läuft automatisch! ✨

---

## 📋 Was das Script macht (Step-by-Step)

### Schritt 1: System Requirements Check
- Prüft Python (3.10+)
- Prüft Node.js (18+)
- Prüft npm
- Prüft Git (optional)
- Prüft NVIDIA GPU

### Schritt 2: Backend Setup
- Erstellt Python Virtual Environment
- Aktiviert venv
- Upgraded pip
- Installiert alle Python Dependencies

### Schritt 3: PyTorch Installation
**Interaktive Auswahl:**
```
Which GPU series do you have?

1. RTX 5090 / RTX 50-series (CUDA 12.8)
2. RTX 4090 / RTX 40-series (CUDA 12.1)
3. RTX 3090 / RTX 30-series (CUDA 11.8)
4. CPU only (no GPU)
5. Let me install manually later

Select your GPU: _
```

Installiert automatisch die richtige PyTorch Version!

### Schritt 4: Frontend Setup
- Installiert alle Node.js Dependencies
- Dauert ca. 5-10 Minuten
- Installiert React, Vite, Tauri CLI, etc.

### Schritt 5: Rust Check
- Prüft ob Rust installiert ist
- Falls nicht: Öffnet Installer-Website
- Prüft Visual Studio Build Tools
- Gibt Anleitung bei fehlenden Tools

### Schritt 6: Final Verification
- Überprüft alle Komponenten
- Zeigt Installation Summary
- Gibt nächste Schritte an

---

## 🎯 Für dich (RTX 5090)

```cmd
# Starte setup.bat
setup.bat

# Bei Schritt 3 (PyTorch):
# Wähle: 1 (RTX 5090 / RTX 50-series)

# Das Script installiert automatisch:
# pip install torch torchvision --index-url https://download.pytorch.org/whl/cu128
```

Fertig! Alles für deine RTX 5090 optimiert! 🔥

---

## ⏱️ Installations-Dauer

| Component | Zeit |
|-----------|------|
| System Checks | < 1 Min |
| Backend Setup | 2-5 Min |
| PyTorch Install | 3-8 Min |
| Frontend Setup | 5-10 Min |
| **Total** | **~15-25 Min** |

*Internet-Geschwindigkeit abhängig*

---

## 🔧 Falls Probleme auftreten

### "Python not found"
**Lösung:**
1. Installiere Python: https://www.python.org/downloads/
2. ✅ Aktiviere "Add Python to PATH"
3. Restart Terminal
4. Run setup.bat again

### "Node.js not found"
**Lösung:**
1. Installiere Node.js: https://nodejs.org/
2. Wähle LTS Version (18+)
3. Restart Terminal
4. Run setup.bat again

### "Rust not found"
**Lösung:**
1. setup.bat bietet an die Website zu öffnen
2. Download rustup-init.exe
3. Installiere Rust
4. Restart Terminal
5. Run setup.bat again (oder direkt zu Frontend)

### "Visual Studio Build Tools not detected"
**Lösung:**
1. setup.bat bietet an die Website zu öffnen
2. Download VS Build Tools
3. Installiere "Desktop development with C++"
4. Restart Terminal

### PyTorch Installation fehlgeschlagen
**Lösung:**
```cmd
cd backend
venv\Scripts\activate
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu128
```

---

## 🎨 Nach dem Setup

### Start Option 1: Separate Terminals (Empfohlen)
```cmd
# Terminal 1 - Backend:
cd backend
run.bat

# Terminal 2 - Frontend:
cd frontend  
run.bat
```

### Start Option 2: Automatic
```cmd
start.bat
```

---

## 📊 Was wird installiert?

### Python Packages:
- FastAPI (Web Framework)
- PyTorch + torchvision (AI/ML)
- Diffusers (Stable Diffusion)
- Transformers (HuggingFace)
- SQLite (Database)
- uvicorn (ASGI Server)
- und mehr... (siehe requirements.txt)

### Node.js Packages:
- React 18 (UI Framework)
- TypeScript (Type Safety)
- Vite (Build Tool)
- Tauri CLI (Desktop Framework)
- Tailwind CSS (Styling)
- Zustand (State Management)
- und mehr... (siehe package.json)

### System Requirements:
- Rust (für Tauri Desktop)
- Visual Studio Build Tools (für Rust auf Windows)

---

## ✅ Vorteile von setup.bat

### Ohne setup.bat (manuell):
```cmd
# Backend:
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu128

# Frontend:
cd frontend
npm install

# Rust check...
# VS Build Tools check...
# Verification...
```
**→ ~20 Schritte, viele Fehlerquellen**

### Mit setup.bat (automatisch):
```cmd
setup.bat
```
**→ 1 Command, alles automatisch! ✨**

---

## 🎉 Zusammenfassung

**setup.bat** macht Installation zum Kinderspiel:

1. **Ein Befehl** - `setup.bat`
2. **Automatische Erkennung** - GPU, Python, Node.js
3. **Interaktive Auswahl** - PyTorch für deine GPU
4. **Komplette Verifikation** - Alles wird gecheckt
5. **Hilfreiche Fehler** - Klare Anweisungen bei Problemen
6. **Ready to Go** - Nach ~20 Min alles fertig!

---

**Probiere es aus! 🚀**

Bei Problemen siehe **TROUBLESHOOTING.md**
