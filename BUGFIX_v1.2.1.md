# AI Studio v1.2.1 - Critical Bugfixes

## 🐛 Behobene Probleme

### 1. Tauri Cargo.toml - Feature `shell-open` existiert nicht

**Problem:**
```
error: package `ai-studio` depends on `tauri` with feature `shell-open` 
but `tauri` does not have that feature.
```

**Ursache:**
In Tauri 2.0 wurde `shell-open` in ein separates Plugin verschoben.

**Lösung:**
```toml
# Vorher (FALSCH):
[dependencies]
tauri = { version = "2.0", features = ["shell-open"] }

# Nachher (RICHTIG):
[dependencies]
tauri = { version = "2.0", features = [] }
tauri-plugin-shell = "2.0"
```

**Datei:** `frontend/src-tauri/Cargo.toml`

---

### 2. Pydantic Warning - `model_` Namespace Konflikt

**Problem:**
```
UserWarning: Field "model_key" in LoadModelRequest has conflict 
with protected namespace "model_".
```

**Ursache:**
Pydantic 2.x reserviert `model_*` als geschützten Namespace für Konfiguration.

**Lösung:**
```python
# Vorher (WARNUNG):
class LoadModelRequest(BaseModel):
    model_key: str

# Nachher (KEIN WARNING):
class LoadModelRequest(BaseModel):
    model_config = {"protected_namespaces": ()}
    
    model_key: str
```

**Datei:** `backend/api/routes.py`

---

### 3. Versions-Updates

Alle Komponenten auf v1.2.0 aktualisiert:
- ✅ `backend/config.py` - APP_VERSION = "1.2.0"
- ✅ `frontend/package.json` - version: "1.2.0"
- ✅ `frontend/src-tauri/Cargo.toml` - version = "1.2.0"

---

## 🚀 Anwendung der Fixes

### Automatisch (Empfohlen):

**Download v1.2.1:**
```cmd
# Lade das neue Backup herunter und ersetze deine Dateien
# Oder git pull wenn du das Repository nutzt
```

### Manuell:

**1. Backend Fix (Pydantic Warning):**
```cmd
# Öffne: backend\api\routes.py
# Zeile 33-34, ersetze:

class LoadModelRequest(BaseModel):
    model_key: str

# Mit:

class LoadModelRequest(BaseModel):
    model_config = {"protected_namespaces": ()}
    
    model_key: str
```

**2. Frontend Fix (Tauri Cargo):**
```cmd
# Öffne: frontend\src-tauri\Cargo.toml
# Zeile 11-12, ersetze:

[dependencies]
tauri = { version = "2.0", features = ["shell-open"] }

# Mit:

[dependencies]
tauri = { version = "2.0", features = [] }
tauri-plugin-shell = "2.0"
```

**3. Lösche Cargo Cache:**
```cmd
cd frontend\src-tauri
rmdir /s /q target
cd ..\..
```

**4. Neustart:**
```cmd
# Backend Terminal (CTRL+C zum Stoppen, dann):
cd backend
venv\Scripts\activate
python main.py

# Frontend Terminal (neues Terminal):
cd frontend
npm run tauri dev
```

---

## ✅ Verifikation

Nach den Fixes solltest du sehen:

**Backend Terminal:**
```
INFO: Starting AI Studio v1.2.0
INFO: Database initialized
INFO: Application startup complete.
```
**Keine Pydantic Warnings mehr!**

**Frontend Terminal:**
```
VITE v5.4.21  ready in 178 ms
➜  Local:   http://localhost:3000/

Compiling tauri...
    Finished dev [unoptimized + debuginfo] target(s) in 45.23s
```
**Keine Cargo Fehler mehr!**

---

## 📦 Was wurde geändert

- `frontend/src-tauri/Cargo.toml` - Shell-Plugin Fix
- `backend/api/routes.py` - Pydantic Namespace Fix
- `backend/config.py` - Version 1.2.0
- `frontend/package.json` - Version 1.2.0
- `frontend/src-tauri/Cargo.toml` - Version 1.2.0

---

## 🔄 Nächste Schritte

Nach erfolgreicher Anwendung der Fixes:

1. **Teste erste Generierung:**
   - Frontend sollte öffnen
   - Gib einen Prompt ein
   - Klicke "Generate"
   - Erste Generierung lädt Model (5-10 Min)

2. **GPU Monitoring prüfen:**
   - Header zeigt RTX 5090 Info
   - VRAM Usage wird angezeigt
   - Temperature Monitoring aktiv

3. **Feedback geben:**
   - Funktioniert die Generierung?
   - Performance wie erwartet?
   - Weitere Probleme?

---

**Status:** Diese Fixes sind kritisch für v1.2.1 und werden im nächsten Release enthalten sein.
