---
phase: 1-1
plan: 02
type: execute
wave: 1
depends_on: 
  - "1-01"
files_modified: 
  - "tests/conftest.py"
  - "tests/pytest.ini"
  - "tests/pyproject.toml"
autonomous: true
requirements: 
  - TEST-01
  - TEST-09

must_haves:
  truths:
    - "Mock Arduino devices can be instantiated"
    - "Mock GitHub releases can be queried"
    - "Mock serial devices can be created"
    - "Synthetic error conditions are available"
  artifacts:
    - path: "tests/conftest.py"
      provides: "Shared fixtures for Arduino, GitHub, serial devices"
      exports: ["mock_device", "mock_github_release", "mock_serial", "error_conditions"]
    - path: "tests/pytest.ini"
      provides: "Pytest configuration for tests/"
      exports: ["markers", "addopts"]
    - path: "tests/pyproject.toml"
      provides: "Pytest + coverage settings for tests/"
      exports: ["tool.pytest.ini_options", "tool.coverage.run"]
  key_links:
    - from: "tests/conftest.py"
      to: "ex_installer/*.py"
      via: "Pytest fixtures injected into test modules"
      pattern: "import.*conftest"
    - from: "tests/pytest.ini"
      to: "tests/"
      via: "Test discovery markers"
      pattern: "testpaths.*tests"
---

<objective>
Create test fixtures and configuration for test discovery
Purpose: Establish shared fixtures and configuration that all unit tests will use
Output: tests/conftest.py with fixtures, tests/pytest.ini, tests/pyproject.toml
</objective>

<execution_context>
@/.planning/PROJECT.md
@/.planning/ROADMAP.md
@/.planning/STATE.md
@/home/pete/.config/opencode/get-shit-done/references/planner-mvp-mode.md
@/home/pete/.config/opencode/get-shit-done/references/user-story-template.md
</execution_context>

<context>
From .planning/phases/1-Foundation/1-RESEARCH.md:
- Mock Arduino device (fake vs real)
- Mock GitHub releases
- Mock serial devices
- Synthetic error conditions
- Pytest fixtures with scope="function" for isolated tests, scope="module" for shared resources

From .planning/phases/1-Foundation/1-CONTEXT.md:
- Mock all external calls (serial, git, network)
- pytest-mock for mocking standard library and third-party modules
- Real tests for critical user-facing paths only (not in Phase 1)

From .planning/ROADMAP.md:
- conftest.py with fixtures for mock devices, releases, serial
- Test data: mock devices, mock releases, synthetic error conditions

From PROJECT.md:
- TEST-01: Unit test infrastructure (pytest with 80%+ coverage)
- TEST-09: Virtual environment usage enforced
</context>

<tasks>

<task type="auto">
  <name>Task 1: Create mock_device fixture for Arduino devices</name>
  <files>tests/conftest.py</files>
  <read_first>
    - .planning/phases/1-Foundation/1-RESEARCH.md (Mock Arduino devices, Mock GitHub Releases patterns)
    - .planning/ROADMAP.md (Appendix B: Mock Arduino Devices)
    - ex_installer/arduino_cli.py (for understanding real ArduinoCLI structure)
  </read_first>
  <acceptance_criteria>
    <automated>python -c "
import sys
sys.path.insert(0, 'tests')
from conftest import MockArduino
mock = MockArduino()
assert mock.device_id == 'MOCK_DEVICE_001'
assert mock.firmware_version == '1.0.0'
print('MockArduino fixture created successfully')
"
</automated>
  </acceptance_criteria>
  <done>
    MockArduino fixture available for testing Arduino device behavior
  </done>
</task>

<task type="auto">
  <name>Task 2: Create mock_github_release fixture for GitHub releases</name>
  <files>tests/conftest.py</files>
  <read_first>
    - .planning/phases/1-Foundation/1-RESEARCH.md (Mock GitHub Releases pattern)
    - .planning/ROADMAP.md (Appendix B: Mock GitHub Releases)
    - ex_installer/git_client.py (for understanding real GitClient structure)
  </read_first>
  <acceptance_criteria>
    <automated>python -c "
import sys
sys.path.insert(0, 'tests')
from conftest import MockGitHubRelease
release = MockGitHubRelease('v1.0.0', [], 'https://api.github.com/repos/test/repo/releases/1', 'https://github.com/test/repo/releases')
assert release.tag_name == 'v1.0.0'
assert len(release.assets) == 0
print('MockGitHubRelease fixture created successfully')
"
</automated>
  </acceptance_criteria>
  <done>
    MockGitHubRelease fixture available for testing GitHub release operations
  </done>
</task>

<task type="auto">
  <name>Task 3: Create mock_serial fixture for serial communication</name>
  <files>tests/conftest.py</files>
  <read_first>
    - .planning/phases/1-Foundation/1-RESEARCH.md (Mocking Serial Communication pattern)
    - .planning/ROADMAP.md (Appendix B: Synthetic Error Conditions)
    - ex_installer/serial_monitor.py (for understanding real serial_monitor structure)
  </read_first>
  <acceptance_criteria>
    <automated>python -c "
import sys
sys.path.insert(0, 'tests')
from conftest import MockSerial
mock = MockSerial()
mock.write('TEST_DATA')
result = mock.read(-1)
assert result == b'TEST_DATA'
print('MockSerial fixture created successfully')
"
</automated>
  </acceptance_criteria>
  <done>
    MockSerial fixture available for testing serial communication operations
  </done>
</task>

<task type="auto">
  <name>Task 4: Create synthetic error condition fixtures</name>
  <files>tests/conftest.py</files>
  <read_first>
    - .planning/phases/1-Foundation/1-RESEARCH.md (Synthetic Error Conditions pattern)
    - .planning/ROADMAP.md (Appendix B: Synthetic Error Conditions)
    - .planning/PROJECT.md (TEST-05: Security testing for input validation)
  </read_first>
  <acceptance_criteria>
    <automated>python -c "
import sys
sys.path.insert(0, 'tests')
from conftest import NetworkError, DiskFullError
err = NetworkError('timeout')
assert str(err) == 'Network error (timeout)'
err2 = DiskFullError(0)
assert str(err2) == 'Disk full: 0 bytes available'
print('Error condition fixtures created successfully')
"
</automated>
  </acceptance_criteria>
  <done>
    NetworkError and DiskFullError fixtures available for error scenario testing
  </done>
</task>

<task type="auto">
  <name>Task 5: Create test markers in tests/pytest.ini</name>
  <files>tests/pytest.ini</files>
  <read_first>
    - .planning/phases/1-Foundation/1-RESEARCH.md (Pytest Configuration Pattern)
    - .planning/phases/1-Foundation/1-CONTEXT.md (Test Isolation Strategy, Mocking Approach)
    - .planning/ROADMAP.md (Test markers: unit, integration, e2e, performance, security)
  </read_first>
  <acceptance_criteria>
    <automated>cat tests/pytest.ini | grep -E "unit:|integration:|e2e:|performance:|security:" > /dev/null && cat tests/pytest.ini | grep -E "unit:|integration:|e2e:|performance:|security:"
</automated>
  </acceptance_criteria>
  <done>
    tests/pytest.ini configured with markers for test categorization
  </done>
</task>

<task type="auto">
  <name>Task 6: Configure tests/pyproject.toml with pytest and coverage</name>
  <files>tests/pyproject.toml</files>
  <read_first>
    - .planning/phases/1-Foundation/1-RESEARCH.md (Pytest Coverage Configuration: pyproject.toml)
    - .planning/phases/1-Foundation/1-CONTEXT.md (Coverage enforcement: Warn but allow CI/CD to pass)
  </read_first>
  <acceptance_criteria>
    <automated>cat tests/pyproject.toml | grep -E "tool\.pytest|tool\.coverage" > /dev/null && cat tests/pyproject.toml | grep -E "tool\.pytest|tool\.coverage"
</automated>
  </acceptance_criteria>
  <done>
    tests/pyproject.toml configured with pytest.ini_options and coverage.run/coverage.report
  </done>
</task>

<task type="auto">
  <name>Task 7: Add pytest configuration to tests/conftest.py</name>
  <files>tests/conftest.py</files>
  <read_first>
    - .planning/phases/1-Foundation/1-RESEARCH.md (Pytest Auto-Discovery, Fixture Scope Management patterns)
    - .planning/phases/1-Foundation/1-CONTEXT.md (Test Discovery Pattern: Auto-discover test_*.py and *_test.py)
  </read_first>
  <acceptance_criteria>
    <automated>cat tests/conftest.py | grep -E "pytest_plugins|import pytest" > /dev/null && cat tests/conftest.py | head -5
</automated>
  </acceptance_criteria>
  <done>
    tests/conftest.py includes pytest configuration and imports
  </done>
</task>

</tasks>

<threat_model>
## Trust Boundaries

| Boundary | Description |
|----------|-------------|
| tests/conftest.py → Application code | Fixtures injected into test modules via pytest injection |

## STRIDE Threat Register

| Threat ID | Category | Component | Disposition | Mitigation Plan |
|-----------|----------|-----------|-------------|-----------------|
| T-1-2-01 | T | Mock Arduino devices | mitigate | No external hardware dependencies |
| T-1-2-02 | T | Mock GitHub releases | mitigate | Static mock data, no network calls |
| T-1-2-03 | T | Mock serial devices | mitigate | No real serial hardware dependencies |
| T-1-2-04 | E | Synthetic error conditions | accept | Error conditions are test data, not production data |

## Package Legitimacy

Fixtures use Python standard library only (Mock, MagicMock, json, time). No external packages required beyond what's already in requirements-python313.txt.

</threat_model>

<verification>
[Overall phase checks]
- MockArduino can be instantiated
- MockGitHubRelease can be instantiated
- MockSerial can be instantiated
- NetworkError and DiskFullError can be instantiated
- tests/pytest.ini configured with markers
- tests/pyproject.toml configured with coverage
- conftest.py includes pytest configuration
</verification>

<success_criteria>
Phase 1-02 complete when:
- MockArduino fixture creates instances with device_id and firmware_version
- MockGitHubRelease fixture creates instances with tag_name and assets
- MockSerial fixture can read/write data
- NetworkError and DiskFullError fixtures create synthetic errors
- tests/pytest.ini configured with markers
- tests/pyproject.toml configured with pytest and coverage
- tests/conftest.py includes pytest configuration
- All fixtures pass automated verification
</success_criteria>

<output>
Create `.planning/phases/1-Foundation/1-02-SUMMARY.md` when done
</output>
