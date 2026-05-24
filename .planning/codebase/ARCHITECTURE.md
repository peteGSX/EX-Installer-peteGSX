# Architecture

**Date:** 2026-05-24

## System Design Pattern

### MVC (Model-View-Controller) with Custom Implementation
- **EXInstaller** - Main application window (View/Controller)
  - Inherits from `customtkinter.CTk`
  - Manages overall application state and navigation
  - Holds references to all view frames

### View-Based Navigation Pattern
- Views stored in `EXInstaller.frames` dictionary
- Fast switching without object recreation
- View data retained across switches
- Pattern: `app.switch_view("view_name")`

---

## Layer Architecture

### Application Layer (ex_installer/)
- **Main Window** - `ex_installer.py` - Root application window
- **CLI Management** - `arduino_cli.py` - Arduino CLI operations
- **Git Operations** - `git_client.py` - Git version control
- **Firmware Tools** - `ex_commandstation.py`, `ex_ioexpander.py`, `ex_turntable.py`
- **File Operations** - `file_manager.py` - File download, extraction, management
- **UI Components** - `common_widgets.py` - Base classes for views
- **Configuration** - `advanced_config.py`, `select_version_config.py`
- **Theme** - `theme/` - Theme definitions and application

### Supporting Modules
- **Product Details** - `product_details.py` - Product information display
- **Common Resources** - `common_fonts.py` - Font management
- **Serial Monitoring** - `serial_monitor.py` - Serial communication monitoring
- **Version** - `version.py` - Application version info
- **Welcome** - `welcome.py` - Welcome view
- **Image Resources** - `images/` - Embedded image assets

---

## Data Flow

### Application Initialization
```
__main__.py
  └─> parse arguments
       └─> main()
            └─> create EXInstaller()
                 └─> initialize views
                      └─> switch_view("welcome")
```

### View Switching Flow
```
EXInstaller.switch_view(view_name)
  └─> Check if view exists
       └─> If yes: show existing frame, hide others
       └─> If no: create new view frame, add to frames dict
            └─> Pack frame
```

### Arduino CLI Workflow
```
ArduinoCLI class
  └─> ThreadedArduinoCLI(thread)
       └─> execute CLI commands via subprocess
            └─> QueueMessage → update UI queue
```

---

## Key Classes & Responsibilities

### EXInstaller (ex_installer.py)
- Main application window
- Manages all view frames
- Holds shared resources (ArduinoCLI, GitClient, preferences)
- Coordinates view navigation

### ArduinoCLI (arduino_cli.py)
- Manages Arduino CLI installations
- Downloads CLI from GitHub releases
- Extracts and configures CLI
- Runs CLI commands in threads
- Manages multiple CLI versions

### GitClient (git_client.py)
- Git operations for Arduino CLI projects
- Clone, pull, check status
- Platform-specific git paths
- Error handling for git failures

### FileManager (file_manager.py)
- Threaded downloader for CLI binaries
- Threaded extractor for CLI packages
- User preferences management
- Log file handling
- Install directory management

### CommonWidgets (common_widgets.py)
- Base WindowLayout class
- CreateToolTip class
- SerialMonitor widget
- View creation helpers

---

## Design Patterns

### Singleton Pattern
- `ArduinoCLI` instance created once in `EXInstaller.__init__`
- `GitClient` instance created once in `EXInstaller.__init__`
- Shared across all views

### Singleton + Factory Pattern
- Views created via `frames` dictionary (factory pattern)
- Each view is a separate class inheriting from `WindowLayout`
- Factory-like access via `frames[view_name]`

### Observer Pattern (Threaded Communication)
- Queue-based communication between threads and UI
- `QueueMessage` namedtuple for thread-safe updates
- UI updates from background threads

### Strategy Pattern
- Threaded operations with timeout
- Configurable time limits per operation
- Thread pool management (single thread with timeout)

---

## Entry Points

### Primary Entry Point
- `ex_installer/__main__.py`
- Entry: `python -m ex_installer [options]`
- Options: `--debug`, `--fake`

### Application Entry
- `EXInstaller()` class instantiation
- Initializes shared resources
- Starts welcome view

### Command Line Arguments
- `-D`, `--debug`: Enable debug logging
- `-F`, `--fake`: Enable fake Arduino device for testing

---

## Directory Structure

```
ex_installer/
├── __init__.py           # Initialization & SSL setup
├── __main__.py           # CLI entry point
├── arduino_cli.py        # Arduino CLI management
├── git_client.py         # Git operations
├── ex_commandstation.py  # CommandStation firmware tools
├── ex_ioexpander.py      # IO Expander tools
├── ex_turntable.py       # Turntable tools
├── file_manager.py       # File operations
├── common_widgets.py     # Base widgets
├── common_fonts.py       # Font management
├── compile_upload.py     # Compilation/upload
├── manage_arduino_cli.py # Arduino CLI management UI
├── select_device.py      # Device selection view
├── select_product.py     # Product selection view
├── select_version_config.py # Version config selection
├── serial_monitor.py     # Serial monitor view
├── advanced_config.py    # Advanced configuration
├── product_details.py    # Product info display
├── theme/                # Theme files
├── images/               # Image assets
└── version.py            # Version info
```

---

## Application Lifecycle

1. **Startup**
   - Parse command-line arguments
   - Initialize logger
   - Create EXInstaller window
   - Apply theme and DPI settings
   - Create shared resources (ArduinoCLI, GitClient)

2. **Welcome View**
   - Display welcome screen
   - Show product selection or advanced options

3. **View Navigation**
   - User selects option
   - `switch_view()` displays appropriate view
   - View retains state across switches

4. **Task Execution**
   - View initiates operation (download, install, flash)
   - Operation runs in background thread
   - Progress updates via queue messages

5. **Shutdown**
   - `mainloop()` exits
   - Logger closes
   - Application terminates
