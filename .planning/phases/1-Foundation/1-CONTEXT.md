# Phase 1 Context - Test Infrastructure

Phase: 1 | Name: Foundation | Date: 2026-05-24

## Domain

Test infrastructure foundation for EX-Installer — pytest setup, CI/CD integration, virtual environment management.

## Locked Requirements

From PROJECT.md:

- Virtual environment must be created during Phase 1 (`venv/` with Python 3.13)
- Virtual environment must be used for all Python work and activated before running tests
- CI/CD must activate virtual environment before running tests
- All dependencies must be installed from requirements files (`requirements.txt`, `requirements-python313.txt`)
- Base test dependencies: pytest, pytest-cov, pytest-mock, pytest-benchmark
- Python 3.13 only
- Tests must pass with virtual environment activated

## Decisions

### Test Discovery Pattern

**Selected:** Auto-discover all `test_*.py` and `*_test.py` files

**Rationale:** Pytest's default behavior provides comprehensive coverage with minimal configuration. Auto-discovery reduces boilerplate and allows flexible test placement throughout the project.

### Coverage Enforcement

**Selected:** Warn but allow CI/CD to pass

**Rationale:** Developers must meet the 80%+ threshold, but blocking CI/CD may impede iterative development. Coverage reports provide visibility without halting progress.

**Enforcement:**
- Generate coverage report on every CI/CD run
- Display coverage summary in PR feedback
- Set up local pre-commit hook to warn if coverage < 80% before commit

### Test Isolation Strategy

**Selected:** Some shared fixtures allowed (e.g., database connection)

**Rationale:** Balance between isolation and practicality. Unit tests should be isolated; integration tests can share fixtures like Arduino CLI connections or git clients.

**Implementation:**
- `conftest.py` in project root for project-wide fixtures (Arduino CLI, git client)
- Individual test files or `tests/conftest.py` for module-specific fixtures
- Use `@pytest.fixture(scope="module")` for shared fixtures, `scope="function"` for isolated tests

### Mocking Approach

**Selected:** Mock all external calls (serial, git, network)

**Rationale:** Fully isolated tests with no external dependencies ensure fast, reliable test execution. External calls (serial communication, git operations, network requests) are mocked to avoid flakiness and speed up test runs.

**Implementation:**
- `pytest-mock` for mocking standard library and third-party modules
- `pytest-subprocess` for mocking subprocess calls
- Mock serial connections in unit tests; real serial tests in dedicated integration test suite
- Mock git operations in unit tests; real git tests in integration suite

### CI/CD Trigger Strategy

**Selected:** Run on every push and pull request

**Rationale:** Catch regressions immediately. Every code change must be validated before merging.

**Implementation:**
- GitHub Actions workflow triggers on `push` and `pull_request` events
- Tests run in virtual environment activated by workflow
- Coverage report included in PR comments

## Canonical References

- PROJECT.md — Project requirements and constraints
- `requirements.txt` — Base Python dependencies
- `requirements-python313.txt` — Python 3.13 specific dependencies
- `ex_installer/__main__.py` — Application entry point
- `ex_installer/serial_monitor.py` — Serial communication example
- `ex_installer/arduino_cli.py` — Arduino CLI integration example

## Code Context

**Existing Architecture:**
- CustomTkinter GUI application (cross-platform: Windows, macOS, Linux)
- Serial communication via PySerial (`serial_monitor.py`)
- Git operations via custom `GitClient` class
- Version management from GitHub releases

**Test Strategy Implications:**
- Mock PySerial calls in unit tests (avoid real hardware dependencies)
- Mock git client in unit tests (avoid actual repository access)
- Mock subprocess calls for package installation
- Real tests for critical user-facing paths only (not in Phase 1)

**Test Distribution (from PROJECT.md):**
- Unit Tests: 30% — Component-level tests (mocked external calls)
- Integration Tests: 30% — Cross-module tests (Arduino CLI, git client)
- E2E Tests: 25% — Complete user journeys
- Performance Tests: 10% — Operation timing
- Security Tests: 5% — Input validation, security testing

## Deferred Ideas

None at this time.

---

**Next Step:** Run `/gsd-plan-phase 1` to create detailed execution plans for Phase 1 deliverables.
