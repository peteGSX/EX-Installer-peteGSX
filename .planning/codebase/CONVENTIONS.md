# Conventions

**Date:** 2026-05-24

## Code Style

### Python Style
- **PEP 8** - Follow standard Python style guide
- **Indentation**: 4 spaces (standard for Python)
- **Line Length**: ~80-100 characters
- **Docstrings**: All modules and functions have docstrings

### Naming Conventions

#### Classes
- **CamelCase**: `EXInstaller`, `ArduinoCLI`, `GitClient`
- **Prefix**: `EX` for EX-Installer specific classes
- **Pattern**: `[Domain][Functionality]` (e.g., `ArduinoCLI`)

#### Functions
- **camelCase**: `get_exception()`, `switch_view()`
- **Prefix**: `get_` for getters, `set_` for setters
- **Pattern**: `[action][what]` (e.g., `switch_view`, `enable_fake_device`)

#### Variables
- **camelCase**: `log_dir`, `time_limit`, `queue`
- **snake_case**: `arduino_cli_lock`, `process_params` (internal)

#### Constants
- **UPPER_CASE**: `arduino_cli_lock`, `QueueMessage`
- **Module-level**: `EXInstallerVersion = "1.0.0"`

---

## Module Organization

### Pattern: Module per Feature
- `arduino_cli.py` - Arduino CLI functionality
- `git_client.py` - Git operations
- `file_manager.py` - File management
- `common_widgets.py` - Common UI components
- `ex_*` - EX-Installer specific features

### Pattern: Views in Separate Files
- `welcome.py` - Welcome view
- `select_device.py` - Device selection view
- `select_product.py` - Product selection view
- `select_version_config.py` - Version config view
- `serial_monitor.py` - Serial monitor view

### Pattern: Shared Resources
- `common_widgets.py` - Base classes reused across views
- `common_fonts.py` - Font management
- `images/` - Image assets
- `theme/` - Theme definitions

---

## Code Structure Patterns

### Class-Based Views
```python
class Welcome(WindowLayout):
    def __init__(self, master):
        super().__init__(master)
        # Initialize UI components
        # Configure widgets
        pass
    
    def on_action(self):
        # Handle user interaction
        pass
```

### Singleton Resources
```python
# In ex_installer.py
class EXInstaller(ctk.CTk):
    acli = ArduinoCLI()          # Shared instance
    git = GitClient()            # Shared instance
    preferences = fm.get_user_preferences()  # Shared config
```

### Threaded Operations
```python
class ThreadedArduinoCLI(Thread):
    def run(self):
        # Run in background thread
        # Use queue for communication
        queue.put(QueueMessage("status", "topic", data))
```

---

## Documentation Conventions

### Module Docstrings
```python
"""
Module description.

Purpose: Brief description of module purpose.

Author: Peter Cole

License: GPL v3
"""
```

### Function Docstrings
```python
def function_name(arg1, arg2):
    """
    Function description.

    Arguments:
        arg1 (type): Description of arg1
        arg2 (type): Description of arg2

    Returns:
        type: Description of return value

    Raises:
        ExceptionType: When error occurs
    """
```

### Class Docstrings
```python
class ClassName:
    """
    Class description.

    Purpose: Brief description.

    Attributes:
        attr1 (type): Description of attr1
    """
```

---

## Logging Conventions

### Logger Access
```python
# Per-module logger
self.log = logging.getLogger(__name__)
```

### Log Levels
- **DEBUG**: Detailed debugging information (shown only with `--debug`)
- **WARNING**: Important warnings
- **INFO**: General information (default)

### Log Format
```
%(asctime)s.%(msecs)03d - %(name)s - %(levelname)s - %(funcName)s: - %(message)s
```

---

## File Organization

### Entry Points
- `ex_installer/__init__.py` - Initialization
- `ex_installer/__main__.py` - CLI entry point

### Resource Files
- `ex_installer/images/` - Embedded images
- `ex_installer/theme/` - Theme definitions

### Configuration
- `requirements.txt` - Python 3.10+ dependencies
- `requirements-python313.txt` - Python 3.13 dependencies
- `dcc-ex-theme.json` - Theme configuration

---

## Version Management

### Version Location
- `ex_installer/version.py` - Version information
- `ex_installer_release.py` - Release generation

### Version Format
- Semantic versioning: `1.0.0`
- Updated in release scripts

---

## Build Conventions

### Build Process
1. Install dependencies from `requirements-python313.txt`
2. Build with PyInstaller
3. Generate Windows installer with InnoSetup
4. Sign and package for release

### Build Artifacts
- Python wheel (`.whl`)
- Windows installer (`.exe` via InnoSetup)
- Release package (`.pyz`)

---

## License

- **GPL v3** - Open source license
- All modules include license header
- References to CommandStation license

---

## Security Conventions

### SSL Handling
- Certificate bundled via PyInstaller MEIPASS
- SSL_CERT_FILE set for frozen applications
- CustomTkinter DPI awareness disabled for Linux

### Input Validation
- No direct user input validation visible
- All inputs processed through UI framework

### Error Handling
- Try-except blocks around file operations
- Exception messages logged but not shown to user
- Graceful degradation for failures

---

## Testing Practices

### No Unit Tests
- No test files found
- Manual testing via command-line interface

### Test Mode
- `--fake` flag enables fake Arduino device
- Allows testing without physical hardware

---

## Code Review Guidelines

1. **Module Organization** - Each feature has dedicated file
2. **Documentation** - All public APIs have docstrings
3. **Thread Safety** - Queue-based communication used
4. **Error Handling** - Try-except around I/O operations
5. **Logging** - All operations logged appropriately
6. **Naming** - Clear, descriptive names
7. **Imports** - Local imports use `from . import` pattern
