---
phase: 1-1
plan: 03
type: tdd
wave: 2
depends_on: 
  - "1-01"
  - "1-02"
files_modified: 
  - "tests/unit/test_thread_safety.py"
  - "tests/conftest.py"
autonomous: true
requirements: 
  - TEST-01

must_haves:
  truths:
    - "ThreadedArduinoCLI can execute commands without race conditions"
    - "QueueMessage can be created and serialized"
    - "ThreadedGitClient can execute git operations without race conditions"
    - "API locks prevent concurrent access"
  artifacts:
    - path: "tests/unit/test_thread_safety.py"
      provides: "Thread safety tests for ThreadedArduinoCLI and ThreadedGitClient"
      exports: ["test_threaded_arduino_cli", "test_queue_message", "test_threaded_git_client"]
    - path: "tests/conftest.py"
      provides: "Thread safety test fixtures"
      exports: ["mock_threaded_arduino_cli", "mock_queue", "mock_threaded_git_client"]
  key_links:
    - from: "tests/unit/test_thread_safety.py"
      to: "ex_installer/arduino_cli.py"
      via: "Pytest fixtures inject ThreadedArduinoCLI"
      pattern: "import.*arduino_cli"
    - from: "tests/unit/test_thread_safety.py"
      to: "ex_installer/git_client.py"
      via: "Pytest fixtures inject ThreadedGitClient"
      pattern: "import.*git_client"
---

<objective>
Test thread safety of ThreadedArduinoCLI and ThreadedGitClient
Purpose: Verify thread safety of critical classes that run background operations
Output: tests/unit/test_thread_safety.py with thread safety tests
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
- ThreadedArduinoCLI runs in separate threads with timeout (default 5 minutes)
- ThreadedGitClient runs pygit2 tasks in separate threads
- QueueMessage namedtuple for thread-safe UI updates
- API locks prevent concurrent access

From ex_installer/arduino_cli.py (lines 56-100):
- ThreadedArduinoCLI is a Thread subclass
- Uses arduino_cli_lock Lock() for synchronization
- Runs run() method in separate thread
- Queues results via QueueMessage

From ex_installer/git_client.py (lines 56-92):
- ThreadedGitClient is a Thread subclass
- Uses api_lock Lock() for synchronization
- Runs task() in separate thread
- Queues results via QueueMessage

From .planning/phases/1-Foundation/1-CONTEXT.md:
- Mock all external calls (serial, git, network)
- pytest-mock for mocking standard library and third-party modules

From .planning/ROADMAP.md:
- test_thread_safety.py: ThreadedArduinoCLI, QueueMessage tests (Critical)
- Tests should run independently
- Tests should be fast (< 10 seconds)
</context>

<tasks>

<task type="tdd">
  <name>Task 1: Write failing test for QueueMessage</name>
  <files>tests/unit/test_thread_safety.py, tests/conftest.py</files>
  <behavior>
    - Test 1: QueueMessage can be created with status, topic, data
    - Test 2: QueueMessage can be serialized/deserialized
    - Test 3: QueueMessage attributes are immutable
    - Test 4: QueueMessage can be compared with another instance
  </behavior>
  <action>
    Create test_thread_safety.py with test_queue_message tests. Write tests first, then implement minimal QueueMessage tests to pass.
    - Import QueueMessage from ex_installer.arduino_cli
    - Create mock queue fixture
    - Test creation, serialization, and comparison
    - Run pytest to confirm failures before implementing fixes
  </action>
  <verify>
    <automated>pytest tests/unit/test_thread_safety.py::test_queue_message -v --tb=short</automated>
  </verify>
  <done>
    test_queue_message tests pass, QueueMessage serialization verified
  </done>
</task>

<task type="tdd">
  <name>Task 2: Write failing test for ThreadedArduinoCLI</name>
  <files>tests/unit/test_thread_safety.py, tests/conftest.py</files>
  <behavior>
    - Test 1: ThreadedArduinoCLI can be instantiated with acli_path, params, queue
    - Test 2: ThreadedArduinoCLI queues start message when run() is called
    - Test 3: ThreadedArduinoCLI queues result message when run() completes successfully
    - Test 4: ThreadedArduinoCLI queues error message when run() fails
    - Test 5: ThreadedArduinoCLI uses arduino_cli_lock for synchronization
  </behavior>
  <action>
    Write test_thread_arduino_cli tests. Create mock ThreadedArduinoCLI using pytest-mock.
    - Mock subprocess.Popen to simulate command execution
    - Test instantiation, run() calls, queue messages
    - Test lock synchronization via threading.Lock assertions
    - Run pytest to confirm failures
  </action>
  <verify>
    <automated>pytest tests/unit/test_thread_safety.py::test_threaded_arduino_cli -v --tb=short</automated>
  </verify>
  <done>
    test_thread_arduino_cli tests pass, ThreadedArduinoCLI thread safety verified
  </done>
</task>

<task type="tdd">
  <name>Task 3: Write failing test for ThreadedGitClient</name>
  <files>tests/unit/test_thread_safety.py, tests/conftest.py</files>
  <behavior>
    - Test 1: ThreadedGitClient can be instantiated with task_name, task, queue, args
    - Test 2: ThreadedGitClient queues info message when run() starts
    - Test 3: ThreadedGitClient queues success message when task completes
    - Test 4: ThreadedGitClient queues error message when task fails
    - Test 5: ThreadedGitClient uses api_lock for synchronization
  </behavior>
  <action>
    Write test_threaded_git_client tests. Create mock ThreadedGitClient using pytest-mock.
    - Mock pygit2 functions to simulate git operations
    - Test instantiation, run() calls, queue messages
    - Test lock synchronization via threading.Lock assertions
    - Run pytest to confirm failures
  </action>
  <verify>
    <automated>pytest tests/unit/test_thread_safety.py::test_threaded_git_client -v --tb=short</automated>
  </verify>
  <done>
    test_threaded_git_client tests pass, ThreadedGitClient thread safety verified
  </done>
</task>

</tasks>

<threat_model>
## Trust Boundaries

| Boundary | Description |
|----------|-------------|
| ThreadedArduinoCLI → System | ThreadedArduinoCLI runs subprocess commands, potential for command injection |
| ThreadedGitClient → Pygit2 | ThreadedGitClient runs git operations, potential for path traversal |

## STRIDE Threat Register

| Threat ID | Category | Component | Disposition | Mitigation Plan |
|-----------|----------|-----------|-------------|-----------------|
| T-1-3-01 | T | ThreadedArduinoCLI | mitigate | Use subprocess with proper shell=False, validate commands |
| T-1-3-02 | T | ThreadedGitClient | mitigate | Use pygit2 with proper validation, prevent path traversal |
| T-1-3-03 | S | Thread safety tests | mitigate | Tests use mocked objects, no real threads executed |

## Package Legitimacy

Tests use Python standard library (threading, logging, json) and pytest-mock. No external packages required.

</threat_model>

<verification>
[Overall phase checks]
- test_queue_message tests pass
- test_thread_arduino_cli tests pass
- test_threaded_git_client tests pass
- QueueMessage serialization verified
- Thread locks verified in tests
</verification>

<success_criteria>
Phase 1-03 complete when:
- test_queue_message tests verify QueueMessage creation, serialization, comparison
- test_thread_arduino_cli tests verify ThreadedArduinoCLI instantiation, run(), queue messages, lock usage
- test_threaded_git_client tests verify ThreadedGitClient instantiation, run(), queue messages, lock usage
- All thread safety tests pass with pytest
</success_criteria>

<output>
Create `.planning/phases/1-Foundation/1-03-SUMMARY.md` when done
</output>
