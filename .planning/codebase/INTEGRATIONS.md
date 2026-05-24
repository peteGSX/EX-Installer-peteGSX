# Integrations

**Date:** 2026-05-24

## External Services

### Arduino CLI Management
- **GitHub Releases** - Downloads Arduino CLI binaries from GitHub
  - Manages multiple versions of Arduino CLI
  - Supports installation, configuration, and updates
  - Platform-specific downloads (Windows, macOS, Linux)

### Git Operations
- **PyGit2** - Git client library
  - Manages `.git` directories for Arduino CLI projects
  - Performs git clone, pull, and other operations
  - Used in `GitClient` class for Arduino CLI version management

### Serial Communication
- **Arduino Board** - Physical Arduino boards via USB serial
  - Communication with CommandStation boards
  - Serial monitor for debugging and logging
  - Firmware flashing via Arduino CLI

### Theme Engine
- **dcc-ex-theme** - Custom theme system
  - Theme definitions stored in `dcc-ex-theme.json`
  - Dynamically applied to GUI components
  - Allows user theming preferences

### Fake Device Mode
- **USB Device Emulation** - For testing purposes
  - `--fake` flag enables fake Arduino USB device
  - Allows testing installer without physical hardware
  - Used in `__main__.py` for demonstration

## Web Services

### HTTP Requests
- **aiohttp** - Async HTTP operations
- **requests** - Synchronous HTTP for Arduino CLI downloads
  - Downloads CLI binaries from GitHub releases
  - Handles redirects and authentication if needed

### Authentication
- **PyJWT** - Token handling for authenticated operations
  - JWT tokens for API authentication
  - Token validation for protected resources

## File Systems

### Arduino CLI Projects
- **Git Repositories** - Local Arduino CLI project directories
  - Located in user home directory or specified paths
  - Version-controlled for each CLI version
  - Managed by `ManageArduinoCLI` class

### User Preferences Storage
- **Platform-specific directories** - User settings storage
  - Windows: `AppData` directories
  - macOS: `Library/Application Support`
  - Linux: `~/.config` or `~/.local/share`
  - Managed by `platformdirs`

### Log Files
- **Log directory** - Application logs
  - Created in install directory: `{install_dir}/logs/`
  - Logs named `ex-installer-YYYYMMDD-HHMMSS.log`
  - Debug and warning levels configurable via `--debug` flag

## APIs & Endpoints

### Arduino CLI API
- No direct REST API - CLI version management via git and file operations
- GitHub Releases API used for downloading CLI binaries
- Manual configuration for CLI paths and settings

## External Tools

### InnoSetup
- Windows installer generation
- Scripted installer creation
- Handles file copying, registry entries, and shortcuts

### PyInstaller Hook Support
- **pyinstaller-hooks-contrib** provides hooks for:
  - PyNaCl (Cython extensions)
  - pygit2 (C bindings)
  - Other native library dependencies

---

## Integration Patterns

### Threaded Operations
- **Arduino CLI commands** run in separate threads
- Queue-based communication for thread-safe updates
- Timeout handling (5 minutes default)
- Thread management in `ThreadedArduinoCLI` class

### View-Based Navigation
- **Frame-based UI** - All views stored in `EXInstaller.frames` dictionary
- Fast switching between views without recreation
- View data retained across switches
- Pattern: `app.switch_view("view_name")`

### Centralized Configuration
- **Preferences** - Single `preferences` dictionary
- **Common widgets** - Shared widget classes in `common_widgets.py`
- **Images** - Centralized image loading in `images/` directory
- **Theme** - Theme applied once at startup
