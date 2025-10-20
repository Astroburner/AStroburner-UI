# Icon Setup für Windows

## Problem

Tauri benötigt Icon-Dateien für das Desktop-Fenster. Diese waren im Repository nicht enthalten.

**Fehler:**
```
`icons/icon.ico` not found; required for generating a Windows Resource file
```

## ✅ Lösung

Die Icons sind jetzt im Repository enthalten in: `frontend/src-tauri/icons/`

### Icons im Download enthalten

Wenn du **v1.2.2** oder neuer downloadest, sind alle Icons bereits vorhanden:

- `icon.png` - 1024x1024 Basis-Icon
- `icon.ico` - Windows Multi-Size Icon
- `32x32.png`, `128x128.png`, etc.

**Keine zusätzlichen Schritte nötig!** ✅

---

## Manuelle Icon-Erstellung (falls nötig)

Falls die Icons fehlen, kannst du sie manuell erstellen:

### Option 1: Download v1.2.2

Lade einfach die neueste Version herunter - Icons sind enthalten.

### Option 2: Online Icon Converter

1. **Erstelle oder lade ein Logo (1024x1024 PNG)**
   - AI-generiert
   - Kostenloses Icon von flaticon.com
   - Eigenes Design

2. **Konvertiere zu .ico:**
   - Besuche: https://www.icoconverter.com/
   - Lade dein PNG hoch
   - Wähle alle Größen: 16, 32, 48, 64, 128, 256
   - Download icon.ico

3. **Kopiere in Projekt:**
   ```cmd
   cd C:\KI_Weltherschaft\Astroburner_UI\V1_2\ai-studio\frontend\src-tauri
   mkdir icons
   copy Downloads\icon.ico icons\
   copy Downloads\icon.png icons\
   ```

### Option 3: Mit GIMP (kostenlos)

1. **Download GIMP:**
   - https://www.gimp.org/downloads/

2. **Icon erstellen:**
   - Öffne GIMP
   - Erstelle 1024x1024 Bild
   - Gestalte dein Icon
   - Exportiere als PNG: `icon.png`
   - Exportiere als ICO: `icon.ico`
     - File → Export As → icon.ico
     - Wähle Microsoft Windows Icon

3. **Kopiere zu:**
   ```cmd
   copy icon.ico C:\KI_Weltherschaft\Astroburner_UI\V1_2\ai-studio\frontend\src-tauri\icons\
   copy icon.png C:\KI_Weltherschaft\Astroburner_UI\V1_2\ai-studio\frontend\src-tauri\icons\
   ```

---

## Placeholder Icons verwenden

Falls du schnell testen willst, erstelle einfache Placeholder Icons:

### Mit Paint (Windows integriert)

1. **Öffne Paint**

2. **Erstelle Basis-Icon:**
   - Größe: 1024x1024
   - Hintergrund: Dunkelblau
   - Text: "AI" in groß
   - Speichern als: `icon.png`

3. **Konvertiere zu ICO:**
   - Öffne icon.png in Paint
   - Größe ändern: 256x256
   - Speichern als: `icon.ico` (Typ: ICO ändern)

4. **Kopiere zu Frontend:**
   ```cmd
   copy icon.png C:\KI_Weltherschaft\Astroburner_UI\V1_2\ai-studio\frontend\src-tauri\icons\
   copy icon.ico C:\KI_Weltherschaft\Astroburner_UI\V1_2\ai-studio\frontend\src-tauri\icons\
   ```

---

## Verifikation

Nach dem Kopieren der Icons:

```cmd
cd C:\KI_Weltherschaft\Astroburner_UI\V1_2\ai-studio\frontend\src-tauri\icons
dir
```

Du solltest mindestens sehen:
```
icon.png
icon.ico
```

**Optional** (für beste Qualität):
```
32x32.png
128x128.png
128x128@2x.png
512x512.png
```

---

## Neustart nach Icon-Setup

1. **Lösche Cargo Cache:**
   ```cmd
   cd C:\KI_Weltherschaft\Astroburner_UI\V1_2\ai-studio\frontend\src-tauri
   rmdir /s /q target
   ```

2. **Starte Frontend neu:**
   ```cmd
   cd C:\KI_Weltherschaft\Astroburner_UI\V1_2\ai-studio\frontend
   npm run tauri dev
   ```

3. **Warte auf Kompilierung:**
   - Erste Kompilierung: 2-5 Minuten
   - Tauri lädt Icon während Build
   - Desktop-Fenster öffnet mit deinem Icon

---

## Icon im Taskbar/Tray

Das Icon erscheint:
- ✅ Im Desktop-Fenster (Titelleiste)
- ✅ In der Windows Taskbar
- ✅ Im Alt+Tab Fenster-Wechsler
- ✅ In der .exe Datei (nach `npm run tauri build`)

---

## Troubleshooting

**Icon wird nicht angezeigt:**
- Lösche `target/` Ordner
- Prüfe `icons/` Pfad ist korrekt
- Stelle sicher icon.ico ist valides ICO-Format

**Build Fehler:**
```
TOML parsing error - icons/icon.ico not found
```
- Prüfe ob Datei existiert: `dir icons\icon.ico`
- Prüfe Pfad in tauri.conf.json

**Icon ist verpixelt:**
- Verwende höhere Auflösung (1024x1024 empfohlen)
- Erstelle Multi-Size ICO mit allen Größen

---

## Empfohlene Icon-Größen

Für beste Qualität auf allen Displays:

| Größe | Verwendung |
|-------|------------|
| 16x16 | Taskbar klein |
| 32x32 | Taskbar normal |
| 48x48 | Desktop-Verknüpfung |
| 64x64 | Alt+Tab |
| 128x128 | High-DPI |
| 256x256 | Ultra High-DPI |

**Windows ICO sollte alle Größen enthalten!**

---

## Links & Resources

- **Icon Converter:** https://www.icoconverter.com/
- **Free Icons:** https://www.flaticon.com/
- **GIMP Download:** https://www.gimp.org/
- **AI Icon Generator:** https://www.brandcrowd.com/maker/logos

---

**Status:** Icons sind ab v1.2.2 im Repository enthalten. Einfach neueste Version downloaden! ✅
