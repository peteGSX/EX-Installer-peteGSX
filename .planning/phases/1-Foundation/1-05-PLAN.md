---
phase: 1-1
plan: 05
type: tdd
wave: 2
depends_on: 
  - "1-01"
  - "1-02"
  - "1-03"
  - "1-04"
files_modified: 
  - "tests/unit/test_git_client.py"
  - "tests/conftest.py"
autonomous: true
requirements: 
  - TEST-01

must_haves:
  truths:
    - "GitClient can clone repositories"
    - "GitClient can pull updates"
    - "GitClient can check repository status"
    - "ThreadedGitClient properly queues git operations"
  artifacts:
    - path: "tests/unit/test_git_client.py"
      provides: "Git client unit tests for clone, pull, status operations"
      exports: ["test_git_client_clone", "test_git_client_pull", "test_git_client_status"]
    - path: "tests/conftest.py"
      provides: "Git client test fixtures"
      exports: ["mock_git_client", "mock_github_release"]
  key_links:
    - from: "tests/unit/test_git_client.py"
      to: "ex_installer/git_client.py"
      via: "Pytest fixtures inject GitClient"
      pattern: "import.*git_client"
    - from: "tests/conftest.py"
      to: "tests/unit/test_git_client.py"
      via: "Pytest fixtures injected"
      pattern: "import.*conftest"
---

<objective>
Test git client operations: clone, pull, and status
Purpose: Verify git operations in GitClient and ThreadedGitClient
Output: tests/unit/test_git_client.py with git client tests
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
- ThreadedGitClient runs pygit2 tasks in separate threads
- Uses api_lock Lock() for synchronization
- Queues results via QueueMessage

From ex_installer/git_client.py (lines 94-341):
- GitClient class for cloning and selecting versions from GitHub repositories
- ThreadedGitClient class for running pygit2 tasks in threads
- Uses pygit2 for git operations

From .planning/phases/1-Foundation/1-CONTEXT.md:
- Mock all external calls (serial, git, network)
- pytest-mock for mocking standard library and third-party modules

From .planning/ROADMAP.md:
- test_git_client.py: Clone, pull, status operations (Critical)
- Tests should run independently
- Tests should be fast (< 10 seconds)

From .planning/phases/1-Foundation/1-RESEARCH.md:
- Mock GitHub releases for testing download operations
</context>

<tasks>

<task type="tdd">
  <name>Task 1: Write failing test for GitClient clone</name>
  <files>tests/unit/test_git_client.py, tests/conftest.py</files>
  <behavior>
    - Test 1: GitClient can be instantiated
    - Test 2: GitClient.clone() can clone a repository
    - Test 3: GitClient.clone() returns the cloned repository path
    - Test 4: GitClient.clone() handles invalid repository URLs
    - Test 5: GitClient.clone() handles network errors
  </behavior>
  <action>
    Write test_git_client_clone tests. Create mock GitClient using pytest-mock.
    - Mock pygit2 functions to simulate repository cloning
    - Test instantiation, clone operation, return values
    - Test error handling for invalid URLs and network errors
    - Run pytest to confirm failures
  </action>
  <verify>
    <automated>pytest tests/unit/test_git_client.py::test_git_client_clone -v --tb=short</automated>
  </verify>
  <done>
    test_git_client_clone tests pass, GitClient clone operations verified
  </done>
</task>

<task type="tdd">
  <name>Task 2: Write failing test for GitClient pull</name>
  <files>tests/unit/test_git_client.py, tests/conftest.py</files>
  <behavior>
    - Test 1: GitClient.pull() can pull latest changes
    - Test 2: GitClient.pull() updates the local repository
    - Test 3: GitClient.pull() returns success status
    - Test 4: GitClient.pull() handles pull errors
    - Test 5: GitClient.pull() handles authentication errors
  </behavior>
  <action>
    Write test_git_client_pull tests. Create mock GitClient using pytest-mock.
    - Mock pygit2 functions to simulate repository updates
    - Test pull operation, updates, success status
    - Test error handling for pull failures and authentication errors
    - Run pytest to confirm failures
  </action>
  <verify>
    <automated>pytest tests/unit/test_git_client.py::test_git_client_pull -v --tb=short</automated>
  </verify>
  <done>
    test_git_client_pull tests pass, GitClient pull operations verified
  </done>
</task>

<task type="tdd">
  <name>Task 3: Write failing test for GitClient status</name>
  <files>tests/unit/test_git_client.py, tests/conftest.py</files>
  <behavior>
    - Test 1: GitClient.status() can check repository status
    - Test 2: GitClient.status() returns uncommitted changes count
    - Test 3: GitClient.status() returns staged changes count
    - Test 4: GitClient.status() returns remote tracking branches
    - Test 5: GitClient.status() handles status errors
  </behavior>
  <action>
    Write test_git_client_status tests. Create mock GitClient using pytest-mock.
    - Mock pygit2 functions to simulate status checking
    - Test status operation, changes count, remote branches
    - Test error handling for status failures
    - Run pytest to confirm failures
  </action>
  <verify>
    <automated>pytest tests/unit/test_git_client.py::test_git_client_status -v --tb=short</automated>
  </verify>
  <done>
    test_git_client_status tests pass, GitClient status operations verified
  </done>
</task>

</tasks>

<threat_model>
## Trust Boundaries

| Boundary | Description |
|----------|-------------|
| GitClient → Git Repository | GitClient interacts with Git repositories, potential for path traversal |
| ThreadedGitClient → Filesystem | ThreadedGitClient runs git commands, potential for command injection |

## STRIDE Threat Register

| Threat ID | Category | Component | Disposition | Mitigation Plan |
|-----------|----------|-----------|-------------|-----------------|
| T-1-5-01 | T | GitClient.clone | mitigate | Validate repository URL, use absolute paths |
| T-1-5-02 | T | ThreadedGitClient | mitigate | Validate git commands, prevent command injection |
| T-1-5-03 | T | GitClient.pull | mitigate | Validate pull parameters, prevent path traversal |
| T-1-5-04 | S | GitClient | mitigate | Verify repository authenticity, prevent cloning malicious repos |

## Package Legitimacy

Tests use Python standard library (subprocess, os, json, tempfile) and pytest-mock. No external packages required beyond pygit2.

</threat_model>

<verification>
[Overall phase checks]
- test_git_client_clone tests pass
- test_git_client_pull tests pass
- test_git_client_status tests pass
- GitClient clone operations verified
- GitClient pull operations verified
- GitClient status operations verified
</verification>

<success_criteria>
Phase 1-05 complete when:
- test_git_client_clone tests verify GitClient repository cloning
- test_git_client_pull tests verify GitClient pull operations
- test_git_client_status tests verify GitClient status checking
- All git client tests pass with pytest
</success_criteria>

<output>
Create `.planning/phases/1-Foundation/1-05-SUMMARY.md` when done
</output>
