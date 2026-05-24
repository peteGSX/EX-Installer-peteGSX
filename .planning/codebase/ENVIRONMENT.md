# Python Virtual Environment Setup

## Prerequisites

- Python 3.13 (as specified in `requirements-python313.txt`)
- pip (comes with Python)
- Virtualenv or venv package

## Installation

### Step 1: Create and activate virtual environment

```bash
# Create virtual environment
python -m venv venv

# Activate on Linux/macOS
source venv/bin/activate

# Activate on Windows
# venv\Scripts\activate
```

### Step 2: Install project dependencies

```bash
# Install base dependencies
pip install -r requirements.txt

# Install Python 3.13 specific dependencies
pip install -r requirements-python313.txt

# Install test dependencies
pip install pytest pytest-cov pytest-mock pytest-benchmark
```

### Step 3: Install additional tools (optional)

```bash
pip install bandit security-tests coverage.py
```

## Usage

### Running the application

```bash
# Activate virtual environment
source venv/bin/activate

# Install dependencies (if not already done)
pip install -r requirements.txt

# Run the application
python ex_installer/main.py  # or appropriate entry point
```

### Running tests

```bash
# Activate virtual environment
source venv/bin/activate

# Install test dependencies (if not already done)
pip install pytest pytest-cov pytest-mock pytest-benchmark

# Run all tests
pytest tests/

# Run tests with coverage
pytest tests/ --cov=. --cov-report=html

# Run specific test file
pytest tests/unit/test_arduino_cli.py

# Run tests with verbose output
pytest tests/ -v

# Run tests on specific platform
pytest tests/e2e/ -k "windows"
```

## Project Structure

```
EX-Installer-peteGSX/
├── venv/                    # Python virtual environment
│   ├── bin/                 # Scripts (activate, pip, etc.)
│   └── ...
├── tests/                   # Test directory
│   ├── unit/
│   ├── integration/
│   ├── e2e/
│   ├── performance/
│   └── security/
├── ex_installer/            # Main application
├── build_app.py             # Build script
├── requirements.txt         # Base dependencies
├── requirements-python313.txt  # Python 3.13 specific dependencies
└── setup.cfg                 # Python configuration
```

## Troubleshooting

### Virtual environment not found

```bash
# Remove and recreate
rm -rf venv
python -m venv venv
source venv/bin/activate
```

### Dependency conflicts

```bash
# Reinstall all dependencies
pip install --upgrade pip
pip install -r requirements.txt
pip install -r requirements-python313.txt
```

### Python version mismatch

```bash
# Check Python version
python --version

# Should be Python 3.13
```

## Best Practices

1. **Always activate virtual environment** before running any Python commands
2. **Commit virtual environment files** to git (venv/, .venv/, etc.)
3. **Use requirements.txt** to track dependencies
4. **Create virtual environment** before installing any dependencies
5. **Test on each platform** with activated virtual environment

## CI/CD Integration

GitHub Actions will:
1. Create virtual environment
2. Install dependencies
3. Run tests with coverage
4. Report results on PRs

See `.github/workflows/` for workflow details.

---

**Last Updated:** 2026-05-24
