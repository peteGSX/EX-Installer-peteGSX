---
phase: 1-1
plan: 01
type: execute
wave: 1
depends_on: []
files_modified: 
  - ".planning/phases/1-Foundation/1-CONTEXT.md"
  - ".planning/phases/1-Foundation/1-RESEARCH.md"
  - "requirements.txt"
  - "requirements-python313.txt"
  - ".gitignore"
  - ".planning/codebase/ENVIRONMENT.md"
autonomous: true
requirements: 
  - TEST-01
  - TEST-09

must_haves:
  truths:
    - "Virtual environment exists and is accessible"
    - "pytest can be imported successfully"
    - "Test directory structure is ready"
    - "pytest configuration files exist and are valid"
  artifacts:
    - path: "venv/"
      provides: "Python virtual environment with Python 3.13"
      min_lines: 0
    - path: "requirements.txt"
      provides: "Base Python dependencies"
      exports: ["pip install"]
    - path: "requirements-python313.txt"
      provides: "Python 3.13 specific dependencies"
      exports: ["pip install"]
    - path: ".planning/codebase/ENVIRONMENT.md"
      provides: "Virtual environment documentation"
      contains: "Virtual environment setup and usage"
    - path: "pytest.ini"
      provides: "Pytest test discovery and configuration"
      exports: ["minversion", "testpaths"]
    - path: "pyproject.toml"
      provides: "Pytest + coverage settings"
      exports: ["tool.pytest.ini_options", "tool.coverage.run"]
  key_links:
    - from: ".planning/phases/1-Foundation/1-CONTEXT.md"
      to: ".planning/phases/1-Foundation/1-RESEARCH.md"
      via: "Research decisions and locked requirements"
      pattern: "locked requirements.*virtual environment.*python 3.13"
---

<objective>
Establish test infrastructure foundation with virtual environment, pytest configuration, and documentation
Purpose: Create the foundational test infrastructure that all subsequent tests will run against
Output: Virtual environment, pytest.ini, pyproject.toml, test directory structure, ENVIRONMENT.md documentation
</objective>

<execution_context>
@/.planning/PROJECT.md
@/.planning/ROADMAP.md
@/.planning/STATE.md
@/home/pete/.config/opencode/get-shit-done/references/planner-mvp-mode.md
@/home/pete/.config/opencode/get-shit-done/references/user-story-template.md
</execution_context>

<context>
From .planning/phases/1-Foundation/1-CONTEXT.md:
- Virtual environment must be created with Python 3.13 in `venv/`
- Virtual environment must be used for all Python work and activated before running tests
- CI/CD must activate virtual environment before running tests
- All dependencies must be installed from requirements files
- Base test dependencies: pytest, pytest-cov, pytest-mock, pytest-benchmark

From .planning/PROJECT.md:
- TEST-01: Unit test infrastructure (pytest with 80%+ coverage)
- TEST-09: Virtual environment usage enforced in all phases

From .planning/codebase/STACK.md:
- Python 3.13 target
- Python 3.13 compatible dependencies available
- PyInstaller 6.13.0 for Python 3.13

From .planning/phases/1-Foundation/1-RESEARCH.md:
- pytest 8.0+ supports Python 3.13+
- pytest-cov 4.0+ supports Python 3.13+
- pytest-mock 3.11+ supports Python 3.13+
- pytest-benchmark 4.0+ supports Python 3.13+
</context>

<tasks>

<task type="auto">
  <name>Task 1: Create Python 3.13 virtual environment in venv/</name>
  <files>venv/</files>
  <read_first>
    - .planning/PROJECT.md (TEST-09: Virtual environment must be created with Python 3.13)
    - .planning/codebase/STACK.md (Python 3.13 target)
  </read_first>
  <acceptance_criteria>
    <automated>python3 -m venv --python /usr/bin/python3.13 venv && python -c "import sys; print(f'Python {sys.version}')" | grep -q "Python 3.13"</automated>
  </acceptance_criteria>
  <done>
    venv/ exists with Python 3.13, activation script works (source venv/bin/activate)
  </done>
</task>

<task type="auto">
  <name>Task 2: Create requirements.txt and requirements-python313.txt</name>
  <files>requirements.txt, requirements-python313.txt</files>
  <read_first>
    - .planning/PROJECT.md (TEST-01: pytest, pytest-cov, pytest-mock, pytest-benchmark)
    - .planning/PROJECT.md (TEST-09: All dependencies from requirements files)
    - .planning/phases/1-Foundation/1-RESEARCH.md (Standard Stack: pytest, pytest-cov, pytest-mock, pytest-benchmark)
  </read_first>
  <acceptance_criteria>
    <automated>grep -E "pytest|pytest-cov|pytest-mock|pytest-benchmark" requirements-python313.txt > /dev/null && cat requirements-python313.txt | head -10</automated>
  </acceptance_criteria>
  <done>
    requirements.txt contains base dependencies, requirements-python313.txt contains pytest and test dependencies
  </done>
</task>

<task type="auto">
  <name>Task 3: Create .gitignore to exclude venv/ from git</name>
  <files>.gitignore</files>
  <read_first>
    - .planning/PROJECT.md (TEST-09: Git must ignore venv/ directory)
    - .planning/phases/1-Foundation/1-RESEARCH.md (Package Legitimacy: pytest, pytest-cov, pytest-mock, pytest-benchmark)
  </read_first>
  <acceptance_criteria>
    <automated>grep -E "venv|\.venv|env" .gitignore > /dev/null && grep -E "venv|\.venv|env" .gitignore</automated>
  </acceptance_criteria>
  <done>
    .gitignore excludes venv/, .venv/, env/ directories as required
  </done>
</task>

<task type="auto">
  <name>Task 4: Create pytest.ini with pytest configuration</name>
  <files>pytest.ini</files>
  <read_first>
    - .planning/phases/1-Foundation/1-RESEARCH.md (Pytest Configuration Pattern: pytest.ini)
    - .planning/PROJECT.md (TEST-01: pytest with 80%+ coverage)
  </read_first>
  <acceptance_criteria>
    <automated>cat pytest.ini | grep -E "minversion.*8|testpaths.*tests" > /dev/null && cat pytest.ini</automated>
  </acceptance_criteria>
  <done>
    pytest.ini configured with minversion 8.0, testpaths = tests, coverage options
  </done>
</task>

<task type="auto">
  <name>Task 5: Create pyproject.toml with pytest and coverage settings</name>
  <files>pyproject.toml</files>
  <read_first>
    - .planning/phases/1-Foundation/1-RESEARCH.md (Pytest Coverage Configuration: pyproject.toml)
    - .planning/PROJECT.md (TEST-01: pytest + pytest-cov + pytest-mock)
  </read_first>
  <acceptance_criteria>
    <automated>cat pyproject.toml | grep -E "tool\.pytest|tool\.coverage" > /dev/null && cat pyproject.toml</automated>
  </acceptance_criteria>
  <done>
    pyproject.toml configured with pytest.ini_options and coverage.run/coverage.report
  </done>
</task>

<task type="auto">
  <name>Task 6: Create test directory structure</name>
  <files>tests/conftest.py, tests/pytest.ini, tests/pyproject.toml</files>
  <read_first>
    - .planning/phases/1-Foundation/1-RESEARCH.md (Test Directory Structure, Pattern 1: Pytest Auto-Discovery, Pattern 2: Fixture Scope Management)
    - .planning/PROJECT.md (TEST-01: 20+ unit tests, TEST-07: CI/CD with automated testing)
    - .planning/ROADMAP.md (Deliverables: tests/conftest.py, tests/pytest.ini, tests/pyproject.toml)
  </read_first>
  <acceptance_criteria>
    <automated>ls -d tests/ tests/conftest.py tests/pytest.ini tests/pyproject.toml > /dev/null && cat tests/conftest.py | head -5</automated>
  </acceptance_criteria>
  <done>
    tests/ directory created with conftest.py, pytest.ini, pyproject.toml
  </done>
</task>

<task type="auto">
  <name>Task 7: Create ENVIRONMENT.md documentation</name>
  <files>.planning/codebase/ENVIRONMENT.md</files>
  <read_first>
    - .planning/PROJECT.md (TEST-09: ENVIRONMENT.md must be created and maintained)
    - .planning/PROJECT.md (TEST-09: Virtual environment usage requirements)
    - .planning/ROADMAP.md (Deliverables: ENVIRONMENT.md created)
  </read_first>
  <acceptance_criteria>
    <automated>cat .planning/codebase/ENVIRONMENT.md | grep -E "virtual environment|venv" > /dev/null && cat .planning/codebase/ENVIRONMENT.md | head -10</automated>
  </acceptance_criteria>
  <done>
    ENVIRONMENT.md documents virtual environment creation, activation, and usage requirements
  </done>
</task>

</tasks>

<threat_model>
## Trust Boundaries

| Boundary | Description |
|----------|-------------|
| venv/ → System Python | Virtual environment isolation ensures test dependencies are isolated from system Python |

## STRIDE Threat Register

| Threat ID | Category | Component | Disposition | Mitigation Plan |
|-----------|----------|-----------|-------------|-----------------|
| T-1-01 | S | venv/ creation | mitigate | python -m venv creates isolated environment |
| T-1-02 | T | requirements.txt | mitigate | Dependencies from verified sources (PyPI) |
| T-1-03 | T | pytest.ini | mitigate | Configuration validated against official pytest docs |
| T-1-04 | E | .gitignore | accept | venv excluded from git (standard practice) |

## Package Legitimacy

All packages verified in .planning/phases/1-Foundation/1-RESEARCH.md:
- pytest: 50M/wk downloads, OK disposition
- pytest-cov: 3M/wk downloads, OK disposition  
- pytest-mock: 5M/wk downloads, OK disposition
- pytest-benchmark: 1M/wk downloads, OK disposition

</threat_model>

<verification>
[Overall phase checks]
- pytest.ini exists and is valid
- pyproject.toml exists and is valid
- venv/ exists with Python 3.13
- All test files are discoverable
</verification>

<success_criteria>
Phase 1-01 complete when:
- venv/ exists with Python 3.13
- requirements.txt and requirements-python313.txt exist
- .gitignore excludes venv/
- pytest.ini configured with pytest 8.0+
- pyproject.toml configured with pytest and coverage
- tests/ directory structure created
- ENVIRONMENT.md documented
- All tasks pass automated verification
</success_criteria>

<output>
Create `.planning/phases/1-Foundation/1-01-SUMMARY.md` when done
</output>
