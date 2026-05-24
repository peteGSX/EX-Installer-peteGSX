---
phase: 1-1
plan: 04
type: tdd
wave: 2
depends_on: 
  - "1-01"
  - "1-02"
  - "1-03"
files_modified: 
  - "tests/unit/test_file_manager.py"
  - "tests/conftest.py"
autonomous: true
requirements: 
  - TEST-01

must_haves:
  truths:
    - "ThreadedDownloader can download files with progress reporting"
    - "ThreadedExtractor can extract archives without race conditions"
    - "FileManager can manage user preferences"
    - "ThreadedDownloader can handle download errors"
  artifacts:
    - path: "tests/unit/test_file_manager.py"
      provides: "File manager unit tests for download, extract, manage operations"
      exports: ["test_threaded_downloader", "test_threaded_extractor", "test_file_manager"]
    - path: "tests/conftest.py"
      provides: "File manager test fixtures"
      exports: ["mock_threaded_downloader", "mock_threaded_extractor", "mock_file_manager"]
  key_links:
    - from: "tests/unit/test_file_manager.py"
      to: "ex_installer/file_manager.py"
      via: "Pytest fixtures inject ThreadedDownloader, ThreadedExtractor"
      pattern: "import.*file_manager"
    - from: "tests/conftest.py"
      to: "tests/unit/test_file_manager.py"
      via: "Pytest fixtures injected"
      pattern: "import.*conftest"
---

<objective>
Test file manager operations: download, extract, and management
Purpose: Verify file operations in ThreadedDownloader and ThreadedExtractor
Output: tests/unit/test_file_manager.py with file manager tests
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
- ThreadedDownloader for CLI binaries download
- ThreadedExtractor for CLI package extraction
- User preferences management

From ex_installer/file_manager.py (from PROJECT.md context):
- ThreadedDownloader: downloads files with progress reporting
- ThreadedExtractor: extracts CLI packages
- FileManager: manages user preferences, log files, install directories

From .planning/phases/1-Foundation/1-CONTEXT.md:
- Mock all external calls (serial, git, network)
- pytest-mock for mocking standard library and third-party modules

From .planning/ROADMAP.md:
- test_file_manager.py: Download, extract, manage operations (Critical)
- Tests should run independently
- Tests should be fast (< 10 seconds)
</context>

<tasks>

<task type="tdd">
  <name>Task 1: Write failing test for ThreadedDownloader</name>
  <files>tests/unit/test_file_manager.py, tests/conftest.py</files>
  <behavior>
    - Test 1: ThreadedDownloader can be instantiated with download_path, params, queue
    - Test 2: ThreadedDownloader queues progress message during download
    - Test 3: ThreadedDownloader queues success message when download completes
    - Test 4: ThreadedDownloader queues error message when download fails
    - Test 5: ThreadedDownloader can handle partial downloads
  </behavior>
  <action>
    Write test_threaded_downloader tests. Create mock ThreadedDownloader using pytest-mock.
    - Mock HTTP request functions to simulate file downloads
    - Test instantiation, download process, queue messages
    - Test error handling and partial downloads
    - Run pytest to confirm failures
  </action>
  <verify>
    <automated>pytest tests/unit/test_file_manager.py::test_threaded_downloader -v --tb=short</automated>
  </verify>
  <done>
    test_threaded_downloader tests pass, ThreadedDownloader operations verified
  </done>
</task>

<task type="tdd">
  <name>Task 2: Write failing test for ThreadedExtractor</name>
  <files>tests/unit/test_file_manager.py, tests/conftest.py</files>
  <behavior>
    - Test 1: ThreadedExtractor can be instantiated with extract_path, params, queue
    - Test 2: ThreadedExtractor queues progress message during extraction
    - Test 3: ThreadedExtractor queues success message when extraction completes
    - Test 4: ThreadedExtractor queues error message when extraction fails
    - Test 5: ThreadedExtractor handles corrupted archives
  </behavior>
  <action>
    Write test_threaded_extractor tests. Create mock ThreadedExtractor using pytest-mock.
    - Mock file extraction functions to simulate archive extraction
    - Test instantiation, extraction process, queue messages
    - Test error handling and corrupted archives
    - Run pytest to confirm failures
  </action>
  <verify>
    <automated>pytest tests/unit/test_file_manager.py::test_threaded_extractor -v --tb=short</automated>
  </verify>
  <done>
    test_threaded_extractor tests pass, ThreadedExtractor operations verified
  </done>
</task>

<task type="tdd">
  <name>Task 3: Write failing test for FileManager</name>
  <files>tests/unit/test_file_manager.py, tests/conftest.py</files>
  <behavior>
    - Test 1: FileManager can be instantiated
    - Test 2: FileManager can manage user preferences
    - Test 3: FileManager can manage log files
    - Test 4: FileManager can manage install directories
    - Test 5: FileManager can handle preference serialization
  </behavior>
  <action>
    Write test_file_manager tests. Create mock FileManager using pytest-mock.
    - Mock file operations to simulate file management
    - Test preference management, log file handling, install directory management
    - Test serialization/deserialization of preferences
    - Run pytest to confirm failures
  </action>
  <verify>
    <automated>pytest tests/unit/test_file_manager.py::test_file_manager -v --tb=short</automated>
  </verify>
  <done>
    test_file_manager tests pass, FileManager operations verified
  </done>
</task>

</tasks>

<threat_model>
## Trust Boundaries

| Boundary | Description |
|----------|-------------|
| ThreadedDownloader → Network | ThreadedDownloader downloads files, potential for malicious downloads |
| ThreadedExtractor → Filesystem | ThreadedExtractor extracts files, potential for path traversal |

## STRIDE Threat Register

| Threat ID | Category | Component | Disposition | Mitigation Plan |
|-----------|----------|-----------|-------------|-----------------|
| T-1-4-01 | T | ThreadedDownloader | mitigate | Validate download URLs, verify file hashes |
| T-1-4-02 | T | ThreadedExtractor | mitigate | Use absolute paths, prevent directory traversal |
| T-1-4-03 | S | ThreadedDownloader | mitigate | Verify file integrity after download |
| T-1-4-04 | S | ThreadedExtractor | mitigate | Extract to designated paths only |

## Package Legitimacy

Tests use Python standard library (shutil, json, tempfile, os) and pytest-mock. No external packages required.

</threat_model>

<verification>
[Overall phase checks]
- test_threaded_downloader tests pass
- test_threaded_extractor tests pass
- test_file_manager tests pass
- ThreadedDownloader operations verified
- ThreadedExtractor operations verified
- FileManager operations verified
</verification>

<success_criteria>
Phase 1-04 complete when:
- test_threaded_downloader tests verify ThreadedDownloader download, progress, success, error handling
- test_threaded_extractor tests verify ThreadedExtractor extraction, progress, success, error handling
- test_file_manager tests verify FileManager preference, log, directory management
- All file manager tests pass with pytest
</success_criteria>

<output>
Create `.planning/phases/1-Foundation/1-04-SUMMARY.md` when done
</output>
