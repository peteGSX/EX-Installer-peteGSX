# Structure

**Date:** 2026-05-24

## Project Layout

```
EX-Installer-peteGSX/
├── build_app.py                    # Build automation script
├── ex_installer_release.py         # Release generation script
├── ex_installer/                   # Main Python application
│   ├── __init__.py                 # Initialization module
│   ├── __main__.py                 # CLI entry point
│   ├── arduino_cli.py              # Arduino CLI management
│   ├── common_fonts.py             # Font management
│   ├── common_widgets.py           # Base widget classes
│   ├── compile_upload.py           # Compilation/upload logic
│   ├── ex_commandstation.py        # CommandStation tools
│   ├── ex_installer.py             # Main application window
│   ├── ex_ioexpander.py            # IO Expander tools
│   ├── ex_turntable.py             # Turntable tools
│   ├── file_manager.py             # File operations
│   ├── git_client.py               # Git operations
│   ├── manage_arduino_cli.py       # Arduino CLI management UI
│   ├── product_details.py          # Product info display
│   ├── select_device.py            # Device selection view
│   ├── select_product.py           # Product selection view
│   ├── select_version_config.py    # Version config selection
│   ├── serial_monitor.py           # Serial monitor view
│   ├── theme/                      # Theme files
│   ├── images/                     # Image assets
│   └── version.py                  # Version info
├── docs/                           # Documentation (Sphinx)
├── docs/conf.py                    # Sphinx configuration
├── build_app.py                    # Build script
├── ex_installer_release.py         # Release script
├── ex_installer0019.sh            # Legacy shell script
├── ex_installer_release.py         # Release generator
├── hook-certifi.py                 # SSL hook for PyInstaller
├── LICENSE                         # License file
├── README.md                       # Project readme
├── requirements-python313.txt      # Python 3.13 dependencies
├── requirements.txt                # Python 3.10+ dependencies
├── setup.cfg                       # Python setup config
└── InnoSetup/                      # Windows installer tools
```

---

## Key Directories

### `ex_installer/`
- Main application code
- All Python modules for GUI functionality
- Contains the actual executable application

### `docs/`
- Documentation source files
- Sphinx configuration (`conf.py`)
- Generated documentation (after `make html`)

### `theme/`
- Theme definitions for CustomTkinter
- `dcc-ex-theme.json` - Theme configuration file
- Allows color and style customization

### `images/`
- Embedded image assets
- Icons and graphical resources
- Bundled into application via PyInstaller

### `InnoSetup/`
- Windows installer templates and scripts
- Used to generate Windows `.exe` installers

---

## File Organization Patterns

### Entry Points
- **Primary:** `ex_installer/__main__.py`
- **Module:** `ex_installer/` - Python package

### Module Naming Convention
- `*_cli.py` - CLI/communication related
- `*_manager.py` - Management functions
- `*_config.py` - Configuration handling
- `*_monitor.py` - Monitoring/display
- `*_widget.py` - UI components

### Class Naming Convention
- `EXInstaller` - Main application
- `ArduinoCLI` - Arduino CLI management
- `GitClient` - Git client
- `FileManager` - File operations
- `WindowLayout` - Base widget class

---

## Import Structure

### Local Imports (from ex_installer/)
```python
from .arduino_cli import ArduinoCLI
from .git_client import GitClient
from .welcome import Welcome
from .file_manager import FileManager as fm
from .common_widgets import WindowLayout
from .images import images
from .theme import theme
```

### External Imports
```python
import customtkinter as ctk
import subprocess
import threading
import json
import logging
```

---

## Configuration Management

### User Preferences
- Stored in platform-specific directories
- Managed by `FileManager.get_user_preferences()`
- Location varies by OS (AppData, Library, .config)

### Application Configuration
- Theme selected via `theme.DCC_EX_THEME`
- DPI scaling disabled for Linux
- SSL certificate path configurable

---

## Logging Structure

### Log Files
- Location: `{install_dir}/logs/ex-installer-YYYYMMDD-HHMMSS.log`
- Format: `%(asctime)s.%(msecs)03d - %(name)s - %(levelname)s - %(funcName)s: - %(message)s`
- Levels: DEBUG (debug flag), WARNING (default)

### Logger Setup
- Configured in `__main__.py`
- Per-view loggers in individual modules
- Access via `logging.getLogger(__name__)`

---

## Thread Safety

### Threaded Operations
- Arduino CLI commands run in threads
- `ThreadedArduinoCLI` class
- Queue-based communication (`QueueMessage` namedtuple)
- Timeout handling (5 minutes default)

### Thread-Local Storage
- Each thread has its own queue
- UI updates from background threads via queue
- Lock usage where needed (`arduino_cli_lock`)

---

## Resource Bundling

### PyInstaller MEIPASS
- Frozen applications access resources via `sys._MEIPASS`
- SSL certificate bundled at runtime
- Images and theme files included in bundle

### Distribution Formats
- **Windows:** `.exe` via InnoSetup
- **macOS/Linux:** Python wheel with embedded resources
- All resources accessible via `sys._MEIPASS` path
