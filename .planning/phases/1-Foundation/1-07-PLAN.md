---
phase: 1-1
plan: 07
type: tdd
wave: 2
depends_on: 
  - "1-01"
  - "1-02"
  - "1-03"
  - "1-04"
  - "1-05"
  - "1-06"
files_modified: 
  - "tests/unit/test_serialization.py"
  - "tests/conftest.py"
autonomous: true
requirements: 
  - TEST-01

must_haves:
  truths:
    - "JSON parsing handles valid and invalid JSON"
    - "Preference handling works correctly"
    - "Serialization/deserialization preserves data integrity"
  artifacts:
    - path: "tests/unit/test_serialization.py"
      provides: "Serialization tests for JSON parsing and preference handling"
      exports: ["test_json_parsing", "test_preference_handling", "test_serialization"]
    - path: "tests/conftest.py"
      provides: "Serialization test fixtures"
      exports: ["mock_preferences", "json_data"]
  key_links:
    - from: "tests/unit/test_serialization.py"
      to: "ex_installer/file_manager.py"
      via: "Pytest fixtures inject serialization operations"
      pattern: "import.*json"
    - from: "tests/conftest.py"
      to: "tests/unit/test_serialization.py"
      via: "Pytest fixtures injected"
      pattern: "import.*conftest"
---

<objective>
Test JSON serialization and preference handling
Purpose: Verify JSON parsing and preference serialization/deserialization
Output: tests/unit/test_serialization.py with serialization tests
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
- Test data: JSON parsing, preference handling
- Mock all external calls in unit tests

From ex_installer/file_manager.py (from PROJECT.md context):
- User preferences management
- Log file handling
- Install directory management

From .planning/phases/1-Foundation/1-CONTEXT.md:
- Mock all external calls (serial, git, network)
- pytest-mock for mocking standard library and third-party modules

From .planning/ROADMAP.md:
- test_serialization.py: JSON parsing, preference handling (High)

From .planning/phases/1-Foundation/1-RESEARCH.md:
- Synthetic error conditions available for testing
</context>

<tasks>

<task type="tdd">
  <name>Task 1: Write failing test for JSON parsing</name>
  <files>tests/unit/test_serialization.py, tests/conftest.py</files>
  <behavior>
    - Test 1: JSON parsing handles valid JSON correctly
    - Test 2: JSON parsing handles invalid JSON with error message
    - Test 3: JSON parsing handles nested objects
    - Test 4: JSON parsing handles arrays
    - Test 5: JSON parsing handles special characters
  </behavior>
  <action>
    Write test_json_parsing tests. Create mock JSON parsing using pytest-mock.
    - Mock json.loads to simulate JSON parsing
    - Test valid JSON, invalid JSON, nested objects, arrays, special characters
    - Test error handling for invalid JSON
    - Run pytest to confirm failures
  </action>
  <verify>
    <automated>pytest tests/unit/test_serialization.py::test_json_parsing -v --tb=short</automated>
  </verify>
  <done>
    test_json_parsing tests pass, JSON parsing verified
  </done>
</task>

<task type="tdd">
  <name>Task 2: Write failing test for preference handling</name>
  <files>tests/unit/test_serialization.py, tests/conftest.py</files>
  <behavior>
    - Test 1: Preference handling can read preferences from file
    - Test 2: Preference handling can write preferences to file
    - Test 3: Preference handling can update specific preferences
    - Test 4: Preference handling can handle missing preferences
    - Test 5: Preference handling can handle invalid preference values
  </behavior>
  <action>
    Write test_preference_handling tests. Create mock preference handling using pytest-mock.
    - Mock file operations to simulate preference file I/O
    - Test reading, writing, updating preferences
    - Test missing preferences and invalid values
    - Run pytest to confirm failures
  </action>
  <verify>
    <automated>pytest tests/unit/test_serialization.py::test_preference_handling -v --tb=short</automated>
  </verify>
  <done>
    test_preference_handling tests pass, preference handling verified
  </done>
</task>

<task type="tdd">
  <name>Task 3: Write failing test for serialization</name>
  <files>tests/unit/test_serialization.py, tests/conftest.py</files>
  <behavior>
    - Test 1: Serialization preserves data integrity
    - Test 2: Deserialization can restore serialized data
    - Test 3: Serialization handles complex data structures
    - Test 4: Deserialization handles missing fields gracefully
    - Test 5: Serialization handles special data types (None, booleans, numbers)
  </behavior>
  <action>
    Write test_serialization tests. Create mock serialization using pytest-mock.
    - Mock json.dumps and json.loads to simulate serialization
    - Test data integrity, restoration, complex structures
    - Test missing fields and special data types
    - Run pytest to confirm failures
  </action>
  <verify>
    <automated>pytest tests/unit/test_serialization.py::test_serialization -v --tb=short</automated>
  </verify>
  <done>
    test_serialization tests pass, serialization verified
  </done>
</task>

</tasks>

<threat_model>
## Trust Boundaries

| Boundary | Description |
|----------|-------------|
| JSON parsing → External data | JSON parsing handles user-provided data, potential for malicious JSON |
| Preference handling → Filesystem | Preference handling writes to user's preference file, potential for path traversal |

## STRIDE Threat Register

| Threat ID | Category | Component | Disposition | Mitigation Plan |
|-----------|----------|-----------|-------------|-----------------|
| T-1-7-01 | T | JSON parsing | mitigate | Validate JSON structure, prevent injection |
| T-1-7-02 | T | Preference handling | mitigate | Validate preference file paths, prevent path traversal |
| T-1-7-03 | S | JSON parsing | mitigate | Validate JSON schema before parsing |
| T-1-7-04 | S | Preference handling | mitigate | Sanitize preference values before writing |

## Package Legitimacy

Tests use Python standard library (json, os, tempfile) and pytest-mock. No external packages required.

</threat_model>

<verification>
[Overall phase checks]
- test_json_parsing tests pass
- test_preference_handling tests pass
- test_serialization tests pass
- JSON parsing verified
- Preference handling verified
- Serialization verified
</verification>

<success_criteria>
Phase 1-07 complete when:
- test_json_parsing tests verify valid/invalid JSON parsing
- test_preference_handling tests verify preference file I/O, updates, missing preferences
- test_serialization tests verify data integrity, restoration, complex structures
- All serialization tests pass with pytest
</success_criteria>

<output>
Create `.planning/phases/1-Foundation/1-07-SUMMARY.md` when done
</output>
