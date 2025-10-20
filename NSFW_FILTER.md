# NSFW Filter Kontrolle

## Problem

Standardmäßig hat Stable Diffusion einen NSFW (Not Safe For Work) Content Filter, der potenziell unangemessene Inhalte blockiert.

**Symptom:**
```
Potential NSFW content was detected in one or more images. 
A black image will be returned instead. 
Try again with a different prompt and/or seed.
```

Das führt zu schwarzen Bildern anstatt der generierten Inhalte.

---

## Lösung - Filter deaktivieren

### ✅ Standardmäßig DEAKTIVIERT in AI Studio

**Der NSFW-Filter ist standardmäßig ausgeschaltet** in diesem Projekt.

**Warum?**
- Du hast volle Kontrolle über deine Generierungen
- Keine False Positives (z.B. Strand, Kunst, Anatomie)
- Für professionelle/künstlerische Anwendungen
- Du bist selbst verantwortlich für deine Prompts

---

## Konfiguration

### Option 1: In config.py (Permanent)

**Datei:** `backend/config.py`

```python
class Settings(BaseSettings):
    # ...
    
    # Content Filtering
    DISABLE_NSFW_FILTER: bool = True  # Filter AUS
    # DISABLE_NSFW_FILTER: bool = False  # Filter AN
```

**Ändern:**
```python
# Filter EINSCHALTEN (schwarze Bilder bei NSFW):
DISABLE_NSFW_FILTER: bool = False

# Filter AUSSCHALTEN (alle Inhalte erlauben):
DISABLE_NSFW_FILTER: bool = True  # ← Standard
```

**Nach Änderung:**
- Backend neu starten: `python main.py`
- Beim Model-Laden wird die neue Einstellung angewendet

---

### Option 2: Mit .env Datei (Flexibel)

**Erstelle:** `backend/.env`

```env
# AI Studio Configuration

# NSFW Filter Control
DISABLE_NSFW_FILTER=true   # Filter aus (Standard)
# DISABLE_NSFW_FILTER=false  # Filter an
```

**Vorteile:**
- Keine Code-Änderung nötig
- Einfach zwischen Einstellungen wechseln
- .env wird von Git ignoriert (nicht committed)

**Nach Änderung:**
- Backend neu starten
- Neue Einstellung wird geladen

---

## Wie der Filter funktioniert

### Technische Details

**Mit Filter (safety_checker aktiv):**
```python
pipeline = StableDiffusionPipeline.from_pretrained(
    "stabilityai/stable-diffusion-xl-base-1.0",
    safety_checker=<SafetyChecker>,  # Prüft jedes Bild
    requires_safety_checker=True
)
```

**Ohne Filter (AI Studio Standard):**
```python
pipeline = StableDiffusionPipeline.from_pretrained(
    "stabilityai/stable-diffusion-xl-base-1.0",
    safety_checker=None,  # Keine Prüfung
    requires_safety_checker=False
)
```

### Was der Filter erkennt

**Der NSFW-Filter prüft auf:**
- Nacktheit
- Explizite Inhalte
- Gewalt
- Andere unangemessene Inhalte

**Problem:** Viele False Positives!
- Strand-Szenen
- Kunst (Skulpturen, Gemälde)
- Medizinische Illustrationen
- Fitness/Sport
- Anatomie-Studien

**Deshalb standardmäßig deaktiviert in AI Studio.**

---

## Überprüfen der aktuellen Einstellung

### Im Backend Log

**Beim Model-Laden:**
```
INFO: Loading model: Stable Diffusion XL
INFO: NSFW filter disabled (safety_checker=None)  ← Filter AUS
INFO: Model loaded successfully
```

oder

```
INFO: Loading model: Stable Diffusion XL
INFO: NSFW filter enabled  ← Filter AN
INFO: Model loaded successfully
```

### Im Code überprüfen

```python
# backend/test_nsfw.py
from config import settings

print(f"NSFW Filter: {'DISABLED' if settings.DISABLE_NSFW_FILTER else 'ENABLED'}")
```

```cmd
cd backend
venv\Scripts\activate
python test_nsfw.py
```

---

## Empfehlungen

### Für Privat/Hobby:
**Filter AUS** (Standard)
- Volle kreative Freiheit
- Keine Überraschungen mit schwarzen Bildern
- Du entscheidest selbst

### Für Kommerziell/Öffentlich:
**Filter AN**
- Sicherer für Arbeitsumgebungen
- Vermeidet unangemessene Inhalte
- Für öffentliche Demos/Präsentationen

### Für Kunst/Professionell:
**Filter AUS**
- Künstlerische Freiheit
- Anatomie-Studien möglich
- Keine Zensur von Kunst

---

## Alternative: Manueller Prompt-Filter

**Statt technischem Filter, verwende selbst Negative Prompts:**

```python
# Prompt
"A beautiful landscape..."

# Negative Prompt (was du NICHT willst)
"nsfw, nude, naked, explicit, adult content, sexual, 
 inappropriate, violence, gore, disturbing"
```

**Vorteile:**
- Du hast volle Kontrolle
- Keine False Positives
- Flexibler als automatischer Filter

---

## Häufige Fragen

### Q: Ist es legal, den Filter zu deaktivieren?

**A:** Ja, vollkommen legal. Du nutzt die Software privat auf deinem eigenen Computer. Du bist selbst verantwortlich für die Inhalte, die du generierst.

### Q: Welche Risiken gibt es?

**A:** 
- **Keine technischen Risiken** - Software funktioniert identisch
- **Inhaltliche Verantwortung liegt bei dir** - Nutze die Software verantwortungsvoll
- **Für kommerzielle Nutzung:** Prüfe Lizenzvereinbarungen der Models

### Q: Kann ich den Filter für einzelne Prompts aktivieren/deaktivieren?

**A:** Aktuell nur global in config.py. 

**Zukünftig geplant:** UI-Toggle für Filter pro Generierung.

### Q: Was passiert wenn Filter aktiviert ist und NSFW erkannt wird?

**A:** 
- Backend gibt schwarzes Bild zurück
- Log zeigt: "Potential NSFW content detected"
- Keine Fehlermeldung, einfach schwarzes Ergebnis
- Lösung: Prompt ändern oder Filter deaktivieren

---

## Code-Referenz

### Model Manager mit Filter-Logik

**Datei:** `backend/core/model_manager.py`

```python
# Configure NSFW filter based on settings
pipeline_kwargs = {
    "torch_dtype": self.dtype,
    "use_safetensors": True,
    "cache_dir": settings.MODELS_DIR
}

# Disable NSFW filter if configured
if settings.DISABLE_NSFW_FILTER:
    pipeline_kwargs["safety_checker"] = None
    pipeline_kwargs["requires_safety_checker"] = False
    logger.info("NSFW filter disabled (safety_checker=None)")
else:
    logger.info("NSFW filter enabled")

self.pipeline = pipeline_class.from_pretrained(
    model_info["model_id"],
    **pipeline_kwargs
)
```

---

## Zusammenfassung

**Standard in AI Studio:**
✅ **NSFW Filter ist DEAKTIVIERT**

**Warum:**
- Volle kreative Kontrolle
- Keine False Positives
- Professionelle/künstlerische Anwendungen

**Ändern wenn nötig:**
1. `backend/config.py` → `DISABLE_NSFW_FILTER = False`
2. Backend neu starten
3. Oder `.env` Datei nutzen

**Empfehlung:**
- Filter aus für private/künstlerische Nutzung
- Filter an für öffentliche/kommerzielle Umgebungen
- Nutze Negative Prompts für granulare Kontrolle

---

**Du hast jetzt volle Kontrolle über den Content-Filter! 🎨**
