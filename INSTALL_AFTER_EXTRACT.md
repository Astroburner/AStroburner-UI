# Installation nach dem Entpacken

## ⚠️ WICHTIG: Nach dem Entpacken des Backups MÜSSEN die Dependencies installiert werden!

Das Backup enthält **keine node_modules** um die Dateigröße klein zu halten.

## 🚀 Schnell-Installation (EMPFOHLEN)

```bash
# 1. In das Projekt-Verzeichnis wechseln
cd C:\KI_Weltherschaft\Astroburner_UI\ai-studio

# 2. Setup-Script ausführen (installiert alles automatisch)
setup.bat
```

Das war's! `setup.bat` installiert automatisch:
- ✅ Python Virtual Environment
- ✅ Backend Dependencies (FastAPI, PyTorch, etc.)
- ✅ Frontend Dependencies (React, Tauri, Dialog Plugin, etc.)
- ✅ System-Checks (Python, Node.js, npm, Rust)

## 📝 Manuelle Installation (falls Setup-Script fehlschlägt)

### Backend Installation:
```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### Frontend Installation:
```bash
cd frontend
npm install
```

**Hinweis:** Das Tauri Dialog Plugin (`@tauri-apps/plugin-dialog`) ist bereits in `package.json` enthalten und wird automatisch mit `npm install` installiert.

## ✅ Überprüfung

Nach der Installation sollten folgende Verzeichnisse existieren:

```
ai-studio/
├── backend/
│   └── venv/              ← Python Virtual Environment
│       └── Lib/
│           └── site-packages/  ← Backend Dependencies
├── frontend/
│   └── node_modules/      ← Frontend Dependencies (inkl. Dialog Plugin)
│       └── @tauri-apps/
│           └── plugin-dialog/  ← Muss existieren!
```

## 🐛 Troubleshooting

### Fehler: "Failed to resolve import @tauri-apps/plugin-dialog"

**Ursache:** Frontend Dependencies wurden nicht installiert

**Lösung:**
```bash
cd frontend
npm install
```

### Backend Warning: "Field model_type has conflict with protected namespace"

**Status:** ✅ Gefixt in v1.6.0
- Die Warning ist harmlos und wurde bereits behoben
- Wird beim nächsten Backend-Start nicht mehr erscheinen

### Rust Compilation Error

**Ursache:** Rust oder Visual Studio Build Tools fehlen

**Lösung:**
1. Rust installieren: https://rustup.rs/
2. Visual Studio Build Tools: https://visualstudio.microsoft.com/downloads/#build-tools-for-visual-studio-2022

## 🎯 Nächste Schritte nach Installation

```bash
# App starten
start.bat

# Oder manuell:
# Terminal 1 (Backend):
cd backend
venv\Scripts\activate
python main.py

# Terminal 2 (Frontend):
cd frontend
npm run tauri dev
```

## 📦 Version

Diese Anleitung gilt für: **AI Studio v1.6.0**

---

Bei Problemen siehe auch: `TROUBLESHOOTING.md`
