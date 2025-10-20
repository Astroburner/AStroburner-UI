# 🔄 Update Anleitung - Von v1.0.1 auf v1.0.2

## Option 1: Neue Version downloaden (Empfohlen)

```
https://page.gensparksite.com/project_backups/ai-studio-v1.0.2-windows-fix.tar.gz
```

Extrahiere und ersetze kompletten Ordner.

---

## Option 2: Nur geänderte Dateien ersetzen

Falls du bereits Änderungen gemacht hast, ersetze nur diese Dateien:

### 1. backend/main.py
**Ändere Zeile 1-9:**

**ALT:**
```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import uvicorn
import logging
from contextlib import asynccontextmanager

from api.routes import router, db
from config import settings
```

**NEU:**
```python
import sys
from pathlib import Path

# Add backend directory to Python path
backend_dir = Path(__file__).parent
sys.path.insert(0, str(backend_dir))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import uvicorn
import logging
from contextlib import asynccontextmanager

from api.routes import router, db
from config import settings
```

---

### 2. frontend/src-tauri/tauri.conf.json
**Entferne Zeile 35 (identifier in bundle):**

**ALT:**
```json
  "bundle": {
    "active": true,
    "targets": "all",
    "icon": [
      "icons/icon.png"
    ],
    "identifier": "com.astroburner.ai-studio",  ← DIESE ZEILE LÖSCHEN
    "windows": {
      "certificateThumbprint": null,
      "digestAlgorithm": "sha256",
      "timestampUrl": ""
    }
  }
```

**NEU:**
```json
  "bundle": {
    "active": true,
    "targets": "all",
    "icon": [
      "icons/icon.png"
    ]
  }
```

---

### 3. Neue Dateien hinzufügen

**backend/run.bat** - Download von:
```
https://page.gensparksite.com/project_backups/ai-studio-v1.0.2-windows-fix.tar.gz
```
Extrahiere und kopiere `backend/run.bat`

**frontend/run.bat** - Download von:
```
https://page.gensparksite.com/project_backups/ai-studio-v1.0.2-windows-fix.tar.gz
```
Extrahiere und kopiere `frontend/run.bat`

**TROUBLESHOOTING.md** - Kompletter Guide für Probleme
(Optional, aber hilfreich)

---

### 4. start.bat aktualisieren (Optional)

Die neue `start.bat` hat bessere Error Checks, aber ist optional.

---

## Nach dem Update

1. **Backend testen:**
```cmd
cd C:\KI_Weltherschaft\Astroburner_UI\ai-studio\backend
run.bat
```

Warte auf: `INFO:     Uvicorn running on http://127.0.0.1:8000`

2. **Frontend testen (neues Terminal):**
```cmd
cd C:\KI_Weltherschaft\Astroburner_UI\ai-studio\frontend
run.bat
```

Beim ersten Mal: 5-10 Minuten Rust Compilation!

---

## Schnelltest

Nachdem beide laufen:

1. Öffne Browser: http://127.0.0.1:8000/docs
   → Sollte FastAPI Swagger UI zeigen

2. Desktop App sollte automatisch starten

---

## Bei Problemen

Lies **TROUBLESHOOTING.md** für alle häufigen Fehler und Lösungen!

---

**Version:** 1.0.2
**Fix für:** ModuleNotFoundError und Tauri Config Error
