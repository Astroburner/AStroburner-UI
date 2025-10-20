# Changelog

All notable changes to AI Studio will be documented in this file.

## [v1.2.0] - 2025-01-20

### ✨ Added
- **Interactive Setup Menu**: setup.bat now shows a menu after installation with 6 quick actions
- **models/ Directory**: Created proper models directory structure in project root (not backend)
  - Added `models/__init__.py` with comprehensive documentation
  - Added `models/README.md` with usage guide, performance benchmarks, and troubleshooting
  - Created subdirectories: sd15, sdxl, sdxl-turbo, flux, pony, illustrious, lora
  - Added .gitkeep files to preserve directory structure in git
- **Quick Actions Menu** in setup.bat:
  1. Start AI Studio (automatic)
  2. Start Backend only
  3. Start Frontend only
  4. Open project folder
  5. View system info
  6. Exit

### 🔧 Changed
- **setup.bat Enhancement**: 
  - Added `cmd /k` wrapper to prevent window from closing on error
  - Improved error handling with better error messages
  - Added interactive menu after setup completion
  - Better user feedback during installation
- **Directory Structure**: Models now stored in `models/` (project root) instead of `backend/models/`
- **.gitignore Update**: Preserve models/ structure while ignoring model files

### 📝 Documentation
- Updated models/README.md with:
  - Storage requirements and VRAM usage
  - Model performance benchmarks for RTX 5090
  - Troubleshooting section
  - Configuration guide
  - Tips for best results

### 🐛 Fixed
- Window closing immediately on setup.bat errors (cmd /k wrapper)
- Models directory path confusion (now clearly in project root)
- Missing __init__.py in models/ directory

## [v1.1.0] - 2025-01-19

### ✨ Added
- **Automated Setup Script** (setup.bat) with 6-step installation process
- **Interactive PyTorch Installation** with GPU-specific menu:
  - RTX 5090 / 50-series (CUDA 12.8)
  - RTX 4090 / 40-series (CUDA 12.1)
  - RTX 3090 / 30-series (CUDA 11.8)
  - CPU only
  - Manual installation option
- **System Requirements Checking**:
  - Python 3.10+ verification
  - Node.js 18+ verification
  - npm verification
  - Git detection (optional)
  - NVIDIA GPU detection
- **Automatic Environment Setup**:
  - Python virtual environment creation
  - Dependency installation
  - PyTorch installation with correct CUDA version
  - Frontend dependencies installation
- **Rust & Build Tools Verification**:
  - Rust installation check
  - Visual Studio Build Tools check
  - Automatic browser opening to installer websites

### 🔧 Changed
- Simplified installation from 20+ manual steps to single command
- 50% reduction in installation time (15-25 min vs 30-40 min manual)
- Better error messages and user guidance

### 📝 Documentation
- Added SETUP_BAT_README.md with complete setup.bat documentation
- Added TROUBLESHOOTING.md with solutions for common issues
- Added RTX_5090_SETUP.md with GPU-specific optimization guide

## [v1.0.0] - 2025-01-18

### ✨ Initial Release

#### Core Features
- **Desktop Application Framework**:
  - Tauri 2.0 for lightweight cross-platform desktop app
  - React 18 + TypeScript frontend
  - FastAPI + Python backend
  - SQLite database for generation history

- **AI Image Generation**:
  - Stable Diffusion 1.5 support
  - SDXL Base support
  - SDXL Turbo support
  - GPU acceleration with CUDA
  - Real-time generation progress
  - Batch generation support

- **GPU Optimization**:
  - RTX 5090 32GB VRAM optimization
  - xFormers memory-efficient attention
  - Attention slicing
  - VAE slicing for ultra-high resolution
  - Lazy model loading
  - Automatic GPU monitoring

- **User Interface**:
  - Modern dark theme with Tailwind CSS
  - Real-time GPU monitoring (VRAM, temp, utilization)
  - Parameter controls (steps, CFG, seed, size)
  - Image gallery with history
  - Generation statistics
  - Prompt and negative prompt inputs

- **Backend Features**:
  - 15+ REST API endpoints
  - Model management system
  - GPU monitoring service
  - Generation queue system
  - Image output management
  - SQLite database for metadata

#### Development Tools
- **Backend Scripts**:
  - run.bat for backend startup
  - Comprehensive system checks
  - GPU status verification
  - Log monitoring

- **Frontend Scripts**:
  - run.bat for frontend startup
  - Backend connection testing
  - Automatic Tauri dev server startup

- **Project Scripts**:
  - start.bat for automatic startup (backend + frontend)
  - Enhanced error handling
  - Progress indicators

#### Documentation
- README.md - Main project documentation
- QUICKSTART.md - Quick start guide
- SETUP.md - Detailed setup instructions
- ARCHITECTURE.md - System architecture
- API.md - API documentation
- MODELS.md - Model guide
- TROUBLESHOOTING.md - Problem solutions
- RTX_5090_SETUP.md - GPU optimization guide

#### Technical Stack
- **Frontend**:
  - Tauri 2.0
  - React 18
  - TypeScript 5.0
  - Tailwind CSS 3.4
  - Zustand (state management)
  - Axios (HTTP client)

- **Backend**:
  - Python 3.10+
  - FastAPI 0.109+
  - PyTorch 2.5+ with CUDA 12.8
  - Diffusers 0.31.0
  - SQLite with aiosqlite
  - Uvicorn ASGI server

- **Build Tools**:
  - Vite 5.0
  - Rust 1.70+
  - npm 10+

---

## Version Format

Versions follow Semantic Versioning (SemVer): MAJOR.MINOR.PATCH

- **MAJOR**: Breaking changes
- **MINOR**: New features (backwards compatible)
- **PATCH**: Bug fixes (backwards compatible)

## Download Links

- **v1.2.0**: https://page.gensparksite.com/project_backups/ai-studio-v1.2.0-interactive-setup.tar.gz (170 KB)
- **v1.1.0**: https://page.gensparksite.com/project_backups/ai-studio-v1.1.0-auto-setup.tar.gz (150 KB)

## Future Roadmap

### Planned Features (v1.3.0+)
- Flux.1 model support
- Pony Diffusion model support
- Illustrious XL model support
- LoRA weights support
- Video generation (Wan model)
- Inpainting/Outpainting
- ControlNet integration
- Image upscaling
- Prompt templates
- Generation presets
- Export to multiple formats

### Planned Improvements
- Improved model switching performance
- Better VRAM management
- Enhanced UI/UX
- More generation parameters
- Advanced settings panel
- Generation history filtering
- Batch operations
- Custom model loading
- Cloud storage integration

---

For questions or issues, see TROUBLESHOOTING.md or open an issue on GitHub.
