# Technology Stack

**Date:** 2026-05-24

## Programming Language

- **Python 3.x** - Primary language for the EX-Installer application
- Target: Python 3.13 (as indicated by `requirements-python313.txt`)
- Compatible with Python 3.10+ (based on dependency versions)

## Core Frameworks

### GUI Framework
- **CustomTkinter** 5.2.2 - Modern GUI framework built on top of tkinter
  - Provides a modern, customizable look and feel
  - Cross-platform support (Windows, macOS, Linux)
  - DPI-aware rendering
  - Appearance modes (light/dark)

### Serialization
- **PyInstaller** 6.7.0 (6.13.0 for Python 3.13) - Application bundling
- **pyinstaller-hooks-contrib** 2024.6 - Cross-platform hook support
  - Enables packaging of C-extension modules (PyNaCl, pygit2)

## External Libraries

### Arduino Tools
- **pyserial** 3.5 - Serial communication with Arduino
- **pygit2** 1.15.0 / 1.18.0 - Git operations for Arduino CLI management
- **cryptography** 42.0.4 / 44.0.3 - Cryptographic operations
- **PyJWT** 2.7.0 / 2.10.1 - JSON Web Token handling
- **PyNaCl** 1.5.0 - Native C++ bindings for cryptography

### HTTP & Networking
- **aiohttp** 3.9.4 - Async HTTP client/server
- **requests** 2.32.2 / 2.32.3 - HTTP library
- **urllib3** 2.2.2 / 2.4.0 - HTTP client
- **yarl** 1.9.2 - URL parsing

### Utilities
- **Pillow** 10.3.0 / 11.2.1 - Image processing and manipulation
- **colorama** 0.4.6 - Cross-platform colored terminal text
- **platformdirs** 4.0.0 - Platform-specific directory locations
- **darkdetect** 0.8.0 - Detect dark mode on macOS
- **pefile** 2023.2.7 - PE file analysis
- **lsprotocol** 2023.0.0 - LSP protocol support

### Text & Processing
- **Jinja2** 3.1.4 / 3.1.6 - Template engine
- **Babel** 2.13.1 / 2.17.0 - Internationalization
- **pyspellchecker** 0.7.2 - Spelling check
- **pyenchant** 3.2.2 - Spelling check with language support
- **roman-numerals-py** 3.1.0 - Roman numeral conversion

### Python Standard Library
- **argparse** - Command-line argument parsing
- **logging** - Logging framework
- **subprocess** - Process spawning
- **threading** - Thread management
- **json** - JSON parsing
- **shutil** - File operations
- **tempfile** - Temporary file handling
- **ctypes** - C library access (Windows DPI scaling)

---

## Build & Packaging

### Build Tools
- **build_app.py** - Python script for application building
- **InnoSetup** - Windows installer creation tool

### Packaging Strategy
1. Source code in `ex_installer/` directory
2. Python packages bundled via PyInstaller
3. Windows installer generated using InnoSetup
4. Linux/macOS distribution via Python wheel

### SSL Certificate Handling
- CustomTkinter DPI awareness disabled for Linux
- SSL certificate bundled at runtime via `sys._MEIPASS`
- Certificate path set in `__init__.py` for frozen applications
