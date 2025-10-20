# Contributing to AI Studio

Vielen Dank für dein Interesse an AI Studio! 🎉

## Wie du beitragen kannst

### 1. Bug Reports

Wenn du einen Bug findest:
1. Check ob der Bug schon gemeldet wurde (GitHub Issues)
2. Erstelle ein neues Issue mit:
   - Beschreibung des Problems
   - Schritte zum Reproduzieren
   - Erwartetes vs. tatsächliches Verhalten
   - System Info (OS, GPU, Python Version)
   - Error Logs (Backend Console + Browser Console)

### 2. Feature Requests

Feature Ideen sind willkommen!
1. Erstelle ein Issue mit Tag "enhancement"
2. Beschreibe das Feature detailliert
3. Erkläre den Use Case

### 3. Code Contributions

#### Setup Development Environment

```bash
# Fork das Repository
git clone https://github.com/YOUR_USERNAME/ai-studio.git
cd ai-studio

# Backend Setup
cd backend
python -m venv venv
source venv/bin/activate  # oder venv\Scripts\activate
pip install -r requirements.txt

# Frontend Setup
cd ../frontend
npm install
```

#### Entwicklungs-Workflow

```bash
# Create Feature Branch
git checkout -b feature/my-new-feature

# Make changes...

# Test Backend
cd backend
python main.py
# Test API Endpoints

# Test Frontend
cd frontend
npm run dev
# Test UI Changes

# Commit
git add .
git commit -m "feat: add my new feature"

# Push
git push origin feature/my-new-feature

# Create Pull Request on GitHub
```

#### Code Style

**Python (Backend):**
- Follow PEP 8
- Use type hints
- Add docstrings
- Keep functions small

**TypeScript (Frontend):**
- Use functional components
- Follow React best practices
- Use TypeScript types
- Keep components modular

#### Commit Messages

Verwende Conventional Commits:
- `feat:` Neues Feature
- `fix:` Bug Fix
- `docs:` Documentation
- `style:` Code Formatting
- `refactor:` Code Refactoring
- `test:` Tests
- `chore:` Build/Dependencies

Beispiele:
```
feat: add video generation support
fix: resolve VRAM overflow on large images
docs: update installation guide
```

### 4. Documentation

Verbesserungen an Dokumentation sind immer willkommen:
- README.md
- SETUP.md
- Code Comments
- API Documentation

### 5. Testing

- Test neue Features gründlich
- Test auf verschiedenen Systemen wenn möglich
- Füge Screenshots hinzu bei UI Changes

## Projekt Struktur

```
ai-studio/
├── backend/              # Python Backend
│   ├── api/             # FastAPI Routes
│   ├── core/            # Core Logic (GPU, Models)
│   ├── models/          # Database Models
│   └── utils/           # Utilities
│
├── frontend/            # React Frontend
│   ├── src/
│   │   ├── components/ # React Components
│   │   ├── hooks/      # State Management
│   │   ├── services/   # API Client
│   │   └── types/      # TypeScript Types
│   └── src-tauri/      # Tauri Desktop
│
└── docs/               # Documentation
```

## Fragen?

- Erstelle ein Issue auf GitHub
- Oder kontaktiere [@Astroburner-AI](https://www.youtube.com/@Astroburner-AI)

---

**Danke für deinen Beitrag! 🚀**
