---
phase: 1-1
plan: 06
type: tdd
wave: 2
depends_on: 
  - "1-01"
  - "1-02"
  - "1-03"
  - "1-04"
  - "1-05"
files_modified: 
  - "tests/unit/test_network.py"
  - "tests/conftest.py"
autonomous: true
requirements: 
  - TEST-01

must_haves:
  truths:
    - "Network timeout handling works correctly"
    - "Connection failure handling works correctly"
    - "Network errors are properly queued"
  artifacts:
    - path: "tests/unit/test_network.py"
      provides: "Network operation tests for timeout and connection failures"
      exports: ["test_network_timeout", "test_connection_failure", "test_network_errors"]
    - path: "tests/conftest.py"
      provides: "Network test fixtures"
      exports: ["mock_network", "mock_request", "error_conditions"]
  key_links:
    - from: "tests/unit/test_network.py"
      to: "ex_installer/*.py"
      via: "Pytest fixtures inject network operations"
      pattern: "import.*requests|import.*urllib3"
    - from: "tests/conftest.py"
      to: "tests/unit/test_network.py"
      via: "Pytest fixtures injected"
      pattern: "import.*conftest"
---

<objective>
Test network operation handling: timeouts and connection failures
Purpose: Verify timeout and failure handling in network operations
Output: tests/unit/test_network.py with network operation tests
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
- Network operations tested in Phase 1: Timeout, connection failure handling
- Mock all network calls in unit tests
- Real tests for critical user-facing paths only (not in Phase 1)

From ex_installer/file_manager.py (from PROJECT.md context):
- ThreadedDownloader for CLI binaries download
- Uses HTTP requests for file downloads

From .planning/phases/1-Foundation/1-CONTEXT.md:
- Mock all external calls (serial, git, network)
- pytest-mock for mocking standard library and third-party modules

From .planning/ROADMAP.md:
- test_network.py: Timeout, connection failure handling (High)

From .planning/phases/1-Foundation/1-RESEARCH.md:
- NetworkError synthetic error condition available
- DiskFullError synthetic error condition available
</context>

<tasks>

<task type="tdd">
  <name>Task 1: Write failing test for network timeout handling</name>
  <files>tests/unit/test_network.py, tests/conftest.py</files>
  <behavior>
    - Test 1: Network operation can handle timeout configuration
    - Test 2: Network operation raises exception when timeout occurs
    - Test 3: Network operation queues timeout error message
    - Test 4: Network operation handles long-running connections
    - Test 5: Network operation retries on timeout with exponential backoff
  </behavior>
  <action>
    Write test_network_timeout tests. Create mock network operation using pytest-mock.
    - Mock HTTP request functions to simulate timeout
    - Test timeout configuration, exception handling, queue messages
    - Test long-running connections and retries
    - Run pytest to confirm failures
  </action>
  <verify>
    <automated>pytest tests/unit/test_network.py::test_network_timeout -v --tb=short</automated>
  </verify>
  <done>
    test_network_timeout tests pass, network timeout handling verified
  </done>
</task>

<task type="tdd">
  <name>Task 2: Write failing test for connection failure handling</name>
  <files>tests/unit/test_network.py, tests/conftest.py</files>
  <behavior>
    - Test 1: Network operation can handle connection refused errors
    - Test 2: Network operation can handle connection timeout errors
    - Test 3: Network operation can handle DNS resolution failures
    - Test 4: Network operation queues connection failure messages
    - Test 5: Network operation retries on connection failure
  </behavior>
  <action>
    Write test_connection_failure tests. Create mock network operation using pytest-mock.
    - Mock HTTP request functions to simulate connection failures
    - Test connection refused, timeout, DNS errors
    - Test message queuing and retries
    - Run pytest to confirm failures
  </action>
  <verify>
    <automated>pytest tests/unit/test_network.py::test_connection_failure -v --tb=short</automated>
  </verify>
  <done>
    test_connection_failure tests pass, connection failure handling verified
  </done>
</task>

<task type="tdd">
  <name>Task 3: Write failing test for network error handling</name>
  <files>tests/unit/test_network.py, tests/conftest.py</files>
  <behavior>
    - Test 1: Network operation can handle HTTP error responses
    - Test 2: Network operation can handle SSL certificate errors
    - Test 3: Network operation can handle invalid URL errors
    - Test 4: Network operation queues network error messages
    - Test 5: Network operation handles multiple consecutive failures
  </behavior>
  <action>
    Write test_network_errors tests. Create mock network operation using pytest-mock.
    - Mock HTTP request functions to simulate various errors
    - Test HTTP errors, SSL errors, invalid URLs
    - Test message queuing and multiple failure handling
    - Run pytest to confirm failures
  </action>
  <verify>
    <automated>pytest tests/unit/test_network.py::test_network_errors -v --tb=short</automated>
  </verify>
  <done>
    test_network_errors tests pass, network error handling verified
  </done>
</task>

</tasks>

<threat_model>
## Trust Boundaries

| Boundary | Description |
|----------|-------------|
| Network operations → External network | Network operations access external resources, potential for malicious sites |

## STRIDE Threat Register

| Threat ID | Category | Component | Disposition | Mitigation Plan |
|-----------|----------|-----------|-------------|-----------------|
| T-1-6-01 | T | Network timeout | mitigate | Validate timeout values, prevent DoS attacks |
| T-1-6-02 | T | Connection failure | mitigate | Validate connection parameters, prevent DoS attacks |
| T-1-6-03 | T | Network errors | mitigate | Validate network operations, prevent malicious requests |
| T-1-6-04 | S | Network operations | mitigate | Use HTTPS only, validate SSL certificates |

## Package Legitimacy

Tests use Python standard library (subprocess, threading, json) and pytest-mock. No external packages required.

</threat_model>

<verification>
[Overall phase checks]
- test_network_timeout tests pass
- test_connection_failure tests pass
- test_network_errors tests pass
- Network timeout handling verified
- Connection failure handling verified
- Network error handling verified
</verification>

<success_criteria>
Phase 1-06 complete when:
- test_network_timeout tests verify timeout configuration, exception handling, queue messages
- test_connection_failure tests verify connection refused, timeout, DNS errors, retries
- test_network_errors tests verify HTTP errors, SSL errors, invalid URLs, multiple failures
- All network operation tests pass with pytest
</success_criteria>

<output>
Create `.planning/phases/1-Foundation/1-06-SUMMARY.md` when done
</output>
