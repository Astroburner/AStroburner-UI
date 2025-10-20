# Changelog

All notable changes to AI Studio will be documented in this file.

## [v1.5.0] - 2025-10-20

### 🎨 Major UI/UX Improvements - History Panel Redesign
- **Compact Layout**: Redesigned History Panel to be significantly more compact
  - All information now visible on single screen (no more excessive scrolling)
  - Grid layout: 1 column on small screens, 2 columns on XL screens
  - Smaller thumbnail size (80x80 → more space efficient)
  - Optimized spacing and padding throughout

### ✨ New Features - Enhanced History Information
- **Download Button Per Image**: Each history entry now has its own download button
  - Quick access: Download directly from history without opening full view
  - Green download icon next to red delete button
- **Scheduler Display**: Shows which scheduler was used for generation
  - Examples: "DPM++ 2M", "Euler", "DDIM"
  - Helps reproduce exact generation settings
- **Denoise Strength Display**: Shows denoise strength for img2img generations
  - Only displayed when img2img was used
  - Format: "0.75" (2 decimal precision)
- **Negative Prompt Display**: Now shows negative prompt if used
  - Expandable section below main details
  - Line-clamp for long prompts with full text on hover

### 🗄️ Backend Enhancements
- **Database Schema**: Added new columns to generations table
  - `scheduler TEXT` - Stores scheduler used
  - `denoise_strength REAL` - Stores img2img strength
  - Automatic migration for existing databases
- **API Updates**: Backend now saves and returns new fields
  - `save_generation()` accepts scheduler and denoise_strength
  - All history queries return complete generation data

### 📊 Information Display (Complete List)
**Now Displayed in History:**
- ✅ Thumbnail (clickable to open full image)
- ✅ Prompt (2-line clamp with hover for full text)
- ✅ Model Key
- ✅ Image Size (Width x Height)
- ✅ Steps
- ✅ CFG Scale (Guidance)
- ✅ Seed (if set)
- ✅ **Scheduler (NEW)**
- ✅ **Denoise Strength (NEW - img2img only)**
- ✅ **Negative Prompt (NEW - expandable section)**
- ✅ Created Date & Time
- ✅ Download & Delete actions

### 🎯 Layout Improvements
- **2-Column Grid on Large Screens**: Better space utilization
- **Smaller Thumbnails**: 80x80px (more compact)
- **Condensed Info Cards**: Tighter spacing, more information density
- **Quick Actions**: Download and delete buttons always visible
- **Responsive Design**: Adapts to screen size (1 or 2 columns)

### 🔧 Technical Changes
- Frontend Generation type extended with `scheduler` and `denoise_strength`
- Database migration handles existing databases gracefully
- API routes pass new fields when saving generations
- Backward compatible with old generations (fields nullable)

---

## [v1.2.2] - 2025-10-20

### 🐛 Critical Fixes
- **Missing Icon Files**: Added complete icon set for Tauri Windows build
  - Error fixed: `icons/icon.ico not found; required for Windows Resource file`
  - Added icon.png (1024x1024 base)
  - Added icon.ico (Windows multi-size: 16, 32, 48, 64, 128, 256)
  - Added 32x32.png, 128x128.png, 128x128@2x.png, 512x512.png
- **Icon Design**: Dark blue theme with "AI" logo
  - Background: #1a1a2e (dark blue)
  - Circle: #16213e (navy)
  - Text: #e94560 (red)

### 📦 Added
- `frontend/src-tauri/icons/` directory with complete icon set
- `create_icons.sh` script for regenerating icons
- `ICON_SETUP_WINDOWS.md` guide for manual icon setup

### 🔧 Updated
- `tauri.conf.json` - version 1.2.0 and all icon paths
- Bundle configuration with complete icon array

---

## [v1.2.1] - 2025-10-20

### 🐛 Critical Fixes
- **Tauri Cargo Error**: Fixed shell-open feature not found
  - Error: `tauri does not have feature shell-open`
  - Solution: Replaced with `tauri-plugin-shell = "2.0"`
  - Tauri 2.0 moved shell to separate plugin
- **Pydantic Warning**: Fixed model_key namespace conflict
  - Warning: `Field "model_key" conflicts with protected namespace "model_"`
  - Solution: Added `model_config = {"protected_namespaces": ()}`
  - Applied to `LoadModelRequest` in `backend/api/routes.py`

### 🔧 Version Updates
- Backend config: APP_VERSION = "1.2.0"
- Frontend package.json: version = "1.2.0"
- Tauri Cargo.toml: version = "1.2.0"

### 📝 Documentation
- Added `BUGFIX_v1.2.1.md` with detailed fix instructions
- Manual and automatic fix procedures documented

---

## [v1.2.0] - 2025-10-20

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

- **v1.2.2** (Latest): https://page.gensparksite.com/project_backups/ai-studio-v1.2.2-with-icons.tar.gz (524 KB) ⭐ **RECOMMENDED**
- **v1.2.1**: https://page.gensparksite.com/project_backups/ai-studio-v1.2.1-bugfixes.tar.gz (192 KB)
- **v1.2.0**: https://page.gensparksite.com/project_backups/ai-studio-v1.2.0-final.tar.gz (182 KB)
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
