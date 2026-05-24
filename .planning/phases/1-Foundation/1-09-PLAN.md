---
phase: 1-1
plan: 09
type: tdd
wave: 2
depends_on: 
  - "1-01"
  - "1-02"
  - "1-03"
  - "1-04"
  - "1-05"
  - "1-06"
  - "1-07"
  - "1-08"
files_modified: 
  - "tests/unit/test_utils.py"
  - "tests/conftest.py"
autonomous: true
requirements: 
  - TEST-01

must_haves:
  truths:
    - "Version comparison works correctly"
    - "Format conversion works correctly"
    - "Utility functions handle edge cases"
  artifacts:
    - path: "tests/unit/test_utils.py"
      provides: "Utility function tests for version comparison and format conversion"
      exports: ["test_version_comparison", "test_format_conversion", "test_utils"]
    - path: "tests/conftest.py"
      provides: "Utility test fixtures"
      exports: ["mock_utils", "version_data"]
  key_links:
    - from: "tests/unit/test_utils.py"
      to: "ex_installer/version.py"
      via: "Pytest fixtures inject utility functions"
      pattern: "import.*version"
    - from: "tests/conftest.py"
      to: "tests/unit/test_utils.py"
      via: "Pytest fixtures injected"
      pattern: "import.*conftest"
---

<objective>
Test utility functions: version comparison and format conversion
Purpose: Verify version comparison and format conversion utility functions
Output: tests/unit/test_utils.py with utility function tests
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
- Test data: Version comparison, format conversion
- Mock all external calls in unit tests

From ex_installer/version.py (from PROJECT.md context):
- Application version info
- Version management

From .planning/phases/1-Foundation/1-CONTEXT.md:
- Mock all external calls (serial, git, network)
- pytest-mock for mocking standard library and third-party modules

From .planning/ROADMAP.md:
- test_utils.py: Version comparison, format conversion (Medium)

From .planning/phases/1-Foundation/1-RESEARCH.md:
- Synthetic error conditions available for testing
</context>

<tasks>

<task type="tdd">
  <name>Task 1: Write failing test for version comparison</name>
  <files>tests/unit/test_utils.py, tests/conftest.py</files>
  <behavior>
    - Test 1: Version comparison handles semantic versioning (e.g., 1.0.0, 1.0.1, 2.0.0)
    - Test 2: Version comparison handles pre-release versions (e.g., 1.0.0-alpha, 1.0.0-beta)
    - Test 3: Version comparison handles post-release versions (e.g., 1.0.0.post1)
    - Test 4: Version comparison handles build versions (e.g., 1.0.0+build1)
    - Test 5: Version comparison handles edge cases (empty strings, None values)
  </behavior>
  <action>
    Write test_version_comparison tests. Create mock version comparison using pytest-mock.
    - Mock version comparison functions to simulate version comparison
    - Test semantic versioning, pre-release, post-release, build versions
    - Test edge cases (empty strings, None values)
    - Run pytest to confirm failures
  </action>
  <verify>
    <automated>pytest tests/unit/test_utils.py::test_version_comparison -v --tb=short</automated>
  </verify>
  <done>
    test_version_comparison tests pass, version comparison verified
  </done>
</task>

<task type="tdd">
  <name>Task 2: Write failing test for format conversion</name>
  <files>tests/unit/test_utils.py, tests/conftest.py</files>
  <behavior>
    - Test 1: Format conversion handles date format conversion
    - Test 2: Format conversion handles number format conversion
    - Test 3: Format conversion handles string formatting
    - Test 4: Format conversion handles edge cases (empty strings, None values)
    - Test 5: Format conversion handles special characters
  </behavior>
  <action>
    Write test_format_conversion tests. Create mock format conversion using pytest-mock.
    - Mock format conversion functions to simulate format conversion
    - Test date format, number format, string formatting
    - Test edge cases (empty strings, None values)
    - Test special character handling
    - Run pytest to confirm failures
  </action>
  <verify>
    <automated>pytest tests/unit/test_utils.py::test_format_conversion -v --tb=short</automated>
  </verify>
  <done>
    test_format_conversion tests pass, format conversion verified
  </done>
</task>

<task type="tdd">
  <name>Task 3: Write failing test for utility functions</name>
  <files>tests/unit/test_utils.py, tests/conftest.py</files>
  <behavior>
    - Test 1: Utility functions handle edge cases (empty input, None values)
    - Test 2: Utility functions handle special characters
    - Test 3: Utility functions return expected values
    - Test 4: Utility functions handle multiple edge cases simultaneously
    - Test 5: Utility functions handle complex data structures
  </behavior>
  <action>
    Write test_utils tests. Create mock utility functions using pytest-mock.
    - Mock utility functions to simulate various utility operations
    - Test edge cases, special characters, expected values
    - Test multiple edge cases simultaneously
    - Test complex data structures
    - Run pytest to confirm failures
  </action>
  <verify>
    <automated>pytest tests/unit/test_utils.py::test_utils -v --tb=short</automated>
  </verify>
  <done>
    test_utils tests pass, utility functions verified
  </done>
</task>

</tasks>

<threat_model>
## Trust Boundaries

| Boundary | Description |
|----------|-------------|
| Version comparison → User input | Version comparison handles user-provided version strings, potential for invalid versions |
| Format conversion → User data | Format conversion handles user-provided data, potential for format injection |

## STRIDE Threat Register

| Threat ID | Category | Component | Disposition | Mitigation Plan |
|-----------|----------|-----------|-------------|-----------------|
| T-1-9-01 | T | Version comparison | mitigate | Validate version format, prevent injection |
| T-1-9-02 | T | Format conversion | mitigate | Validate format conversion inputs, prevent injection |
| T-1-9-03 | S | Version comparison | mitigate | Sanitize version strings before comparison |
| T-1-9-04 | S | Format conversion | mitigate | Sanitize format conversion inputs before processing |

## Package Legitimacy

Tests use Python standard library (re, json, datetime) and pytest-mock. No external packages required.

</threat_model>

<verification>
[Overall phase checks]
- test_version_comparison tests pass
- test_format_conversion tests pass
- test_utils tests pass
- Version comparison verified
- Format conversion verified
- Utility functions verified
</verification>

<success_criteria>
Phase 1-09 complete when:
- test_version_comparison tests verify semantic versioning, pre-release, post-release, build versions, edge cases
- test_format_conversion tests verify date format, number format, string formatting, edge cases, special characters
- test_utils tests verify edge cases, special characters, expected values, complex data structures
- All utility function tests pass with pytest
</success_criteria>

<output>
Create `.planning/phases/1-Foundation/1-09-SUMMARY.md` when done
</output>
