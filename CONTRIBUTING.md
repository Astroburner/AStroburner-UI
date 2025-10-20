# Contributing to AI Studio

Vielen Dank für Dein Interesse an AI Studio! 🎉

## 🚀 Quick Start

### Voraussetzungen
- Python 3.10+
- Node.js 18+
- Rust 1.70+ (für Tauri)
- NVIDIA GPU mit CUDA Support (empfohlen)

### Setup
```bash
# 1. Repository klonen
git clone https://github.com/Astroburner/AStroburner-UI.git
cd AStroburner-UI

# 2. Setup ausführen
setup.bat
```

## 📋 Code Struktur

```
ai-studio/
├── backend/           # Python FastAPI Backend
│   ├── api/          # API Routes
│   ├── core/         # Model Manager, GPU Monitor
│   ├── models/       # Database Models
│   └── config.py     # Konfiguration
├── frontend/         # Tauri + React Frontend
│   ├── src/         # React Components
│   ├── src-tauri/   # Rust Tauri Backend
│   └── public/      # Static Assets
└── docs/            # Dokumentation
```

## 🔧 Development Workflow

### Backend Development
```bash
cd backend
venv\Scripts\activate
python main.py
```

### Frontend Development
```bash
cd frontend
npm run tauri dev
```

## 📝 Coding Standards

### Python (Backend)
- **Style Guide:** PEP 8
- **Type Hints:** Verwende Type Hints wo möglich
- **Docstrings:** Google-Style Docstrings
- **Formatting:** Black (line length 100)

### TypeScript (Frontend)
- **Style Guide:** Airbnb Style Guide
- **Type Safety:** Strikte TypeScript Konfiguration
- **Components:** Funktionale Komponenten mit Hooks
- **Styling:** Tailwind CSS

### Rust (Tauri)
- **Style Guide:** Rust Standard Style
- **Formatting:** `rustfmt`
- **Linting:** `clippy`

## 🐛 Bug Reports

Bitte verwende die [Bug Report Template](.github/ISSUE_TEMPLATE/bug_report.md) und füge folgende Informationen hinzu:
- OS und Version
- GPU Modell und VRAM
- AI Studio Version
- Reproduktionsschritte
- Logs (falls verfügbar)

## ✨ Feature Requests

Bitte verwende die [Feature Request Template](.github/ISSUE_TEMPLATE/feature_request.md) und beschreibe:
- Das Problem / Use Case
- Vorgeschlagene Lösung
- Alternativen
- Mockups (falls möglich)

## 🔄 Pull Request Process

1. **Fork** das Repository
2. **Branch** erstellen (`git checkout -b feature/AmazingFeature`)
3. **Commit** Deine Änderungen (`git commit -m 'Add some AmazingFeature'`)
4. **Push** zum Branch (`git push origin feature/AmazingFeature`)
5. **Pull Request** öffnen

### PR Checklist
- [ ] Code folgt dem Style Guide
- [ ] Tests wurden hinzugefügt/aktualisiert
- [ ] Dokumentation wurde aktualisiert
- [ ] Commit-Messages sind aussagekräftig
- [ ] Branch ist up-to-date mit `main`

## 🧪 Testing

### Backend Tests
```bash
cd backend
pytest
```

### Frontend Tests
```bash
cd frontend
npm run test
```

## 📚 Dokumentation

Wenn Du Code-Änderungen vornimmst, bitte aktualisiere auch:
- README.md (falls nötig)
- Code-Kommentare
- Docstrings
- API-Dokumentation

## 🎨 Design Guidelines

### UI/UX
- **Dark Theme First:** Design für Dark Mode
- **Responsive:** Alle Komponenten müssen responsive sein
- **Accessibility:** WCAG 2.1 Level AA
- **Performance:** Lazy Loading für große Listen

### Icons
- Verwende React Icons (`react-icons`)
- Konsistente Icon-Größen (16px, 20px, 24px)

## 🔐 Security

Wenn Du ein Security-Problem findest:
- **NICHT** als Issue posten
- Kontaktiere direkt: [Deine E-Mail]
- Verwende PGP wenn möglich

## 📄 Lizenz

By contributing, you agree that your contributions will be licensed under the MIT License.

## 🙏 Danke!

Jeder Beitrag, egal wie klein, ist willkommen und geschätzt! 💚

---

**Fragen?** Öffne ein Issue oder kontaktiere uns auf Discord.
