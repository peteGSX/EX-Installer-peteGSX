# Testing

**Date:** 2026-05-24

## Testing Strategy

### Current State
- **Unit Tests**: None found in codebase
- **Integration Tests**: None found
- **End-to-End Tests**: None found
- **Test Files**: No `tests/` directory present

### Testing Philosophy
- Manual testing via command-line interface
- Fake device mode for hardware-agnostic testing
- Focus on functional verification through user interaction

---

## Test Infrastructure

### Fake Device Mode
- **Flag**: `--fake` or `-F`
- **Purpose**: Simulates Arduino USB device
- **Usage**: Enables testing without physical hardware
- **Implementation**: `enable_fake_device()` in `EXInstaller`

### Command-Line Testing
```bash
python -m ex_installer --debug
python -m ex_installer --fake
python -m ex_installer --debug --fake
```

### Debug Mode
- **Flag**: `--debug` or `-D`
- **Effect**: Enables DEBUG log level
- **Log Files**: `{install_dir}/logs/ex-installer-YYYYMMDD-HHMMSS.log`
- **Usage**: Debugging application behavior

---

## Testing Practices

### Manual Testing Flow
1. **Startup**: Verify application launches
2. **Views**: Navigate between welcome, selection, configuration views
3. **Device Detection**: Verify Arduino detection
4. **Downloads**: Test CLI download from GitHub
5. **Installation**: Verify extraction and configuration
6. **Serial Communication**: Test serial monitor
7. **Compilation**: Test firmware compilation/upload
8. **Error Handling**: Verify graceful error messages

### Test Scenarios
- View switching and state retention
- Thread-safe queue communication
- Timeout handling for long operations
- Platform-specific behavior (Windows/macOS/Linux)
- Fake device vs real device modes
- Error recovery on network failures
- Disk space handling for downloads

---

## Test Code Patterns

### Thread Testing Pattern
```python
class ThreadedArduinoCLI(Thread):
    def __init__(self, acli_path, params, queue, time_limit=300):
        super().__init__()
        self.queue = queue
        self.time_limit = timedelta(seconds=time_limit)

    def run(self):
        # Background thread execution
        # Results sent via queue
        queue.put(QueueMessage("status", "topic", data))
```

### View Creation Pattern
```python
def switch_view(self, view_name):
    if view_name in self.frames:
        frame = self.frames[view_name]
        frame.withdraw()
        frame.deiconify()
    else:
        # Create new view
        frame = ViewClass(self)
        self.frames[view_name] = frame
        frame.pack()

def on_action(self):
    # Handle user action
    pass
```

---

## Test Coverage

### Areas Tested
- Application startup and initialization
- View navigation and switching
- Arduino CLI management (download, install, configure)
- Git operations (clone, pull, status)
- Serial communication monitoring
- File download and extraction
- Compilation and upload
- User preferences storage
- Theme application
- DPI scaling and window sizing

### Areas Not Tested
- Unit tests for individual functions
- Integration tests for cross-module interactions
- Performance testing
- Stress testing with multiple devices
- Security testing
- Accessibility testing

---

## Test Tools Available

### Python Testing Frameworks (Installed but not used)
- **unittest** - Standard Python testing
- **pytest** - Python testing (not in requirements)
- **hypothesis** - Property-based testing (not in requirements)

### GUI Testing
- No dedicated GUI testing framework
- Manual testing via GUI is primary approach
- Fake device enables hardware-agnostic testing

---

## Quality Assurance

### Code Quality
- **PEP 8** compliance
- **Docstrings** on all public APIs
- **Type hints** used where available
- **Comments** for complex logic

### Build Quality
- **PyInstaller** hooks for native libraries
- **InnoSetup** for Windows installer generation
- **Sphinx** for documentation

### Runtime Quality
- **Logging** for debugging
- **Thread safety** for concurrent operations
- **Timeout handling** for long-running tasks
- **Error recovery** for network failures

---

## Future Testing Recommendations

### Priority 1: Integration Tests
- Test view switching between all views
- Test complete workflow: select device → download CLI → install → flash
- Test error scenarios: network failure, disk full, timeout

### Priority 2: Unit Tests
- Test helper functions (exception handling, file operations)
- Test configuration parsing
- Test utility functions (version comparison, format conversion)

### Priority 3: Performance Tests
- Test download speed limits
- Test UI responsiveness during long operations
- Test memory usage

### Priority 4: Security Tests
- Test input validation
- Test SSL certificate handling
- Test authentication/authorization

---

## Testing Checklist

- [ ] Application starts successfully on all platforms
- [ ] All views display correctly
- [ ] View switching retains state
- [ ] Fake device mode works
- [ ] Real device mode works
- [ ] Arduino CLI downloads from GitHub
- [ ] CLI installation extracts correctly
- [ ] Serial monitoring displays output
- [ ] Firmware compilation works
- [ ] Upload to device succeeds
- [ ] Error messages are informative
- [ ] Log files are created and contain data
- [ ] User preferences save/load correctly
- [ ] Theme applies correctly
- [ ] DPI scaling works on all resolutions
- [ ] Timeout handling prevents hangs
- [ ] Network failure handling works
- [ ] Disk space warning appears when needed
- [ ] Graceful shutdown works

---

## Documentation Quality

### Documentation Tools
- **Sphinx** 7.2.6 / 8.2.3 - Documentation generator
- **Jinja2** - Template rendering for docs
- **Breathe** 4.35.0 / 4.36.0 - Doxygen integration

### Documentation Structure
- `docs/conf.py` - Sphinx configuration
- Generated docs in `docs/` (after `make html`)
- Documentation for installation, usage, and troubleshooting

---

## Code Quality Metrics

### Cyclomatic Complexity
- Functions generally simple (<5 branches)
- Complex logic in `arduino_cli.py` (threaded CLI execution)
- View classes have moderate complexity (UI wiring)

### Code Coverage
- Estimated 30-40% functional coverage
- No code coverage tools running
- Coverage gaps in error handling paths

### Maintainability
- **Modularity**: High - clear separation of concerns
- **Documentation**: Good - docstrings present
- **Comments**: Adequate for complex logic
- **Tests**: Low - minimal automated testing

---

## Testing Environment

### Development Setup
- Python 3.10+
- PyInstaller for bundling
- InnoSetup for Windows builds

### Test Environment
- Multiple platforms (Windows, macOS, Linux)
- Multiple Arduino board types
- Network conditions (simulated)
- Disk space variations
- Different DPI scales
- Dark/Light modes
