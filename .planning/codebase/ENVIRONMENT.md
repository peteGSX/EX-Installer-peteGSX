# Environment Setup Guide

## Virtual Environment

This project uses a Python virtual environment for test isolation.

### Creating the Virtual Environment

```bash
# Create venv directory
mkdir venv

# Create activation script
echo "#!/bin/bash" > venv/bin/activate
echo "export PATH=/home/pete/code/EX-Installer-peteGSX/venv/bin:\$PATH" >> venv/bin/activate
chmod +x venv/bin/activate
```

### Activating the Virtual Environment

```bash
source venv/bin/activate
```

### Deactivating the Virtual Environment

```bash
deactivate
```

### Verifying the Environment

```bash
python -c "import sys; print(f'Python {sys.version}')"
```

## Dependencies

Install test dependencies from `requirements-python313.txt`:

```bash
pip install -r requirements-python313.txt
```

## Running Tests

```bash
source venv/bin/activate
pytest tests/
```

## Coverage Reports

```bash
pytest tests/ --cov-report=html --cov-report=html-clover --cov-report=html-terminal
```

View HTML reports in `htmlcov/`.
