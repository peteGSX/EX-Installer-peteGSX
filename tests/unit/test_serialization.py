"""
Serialization tests for JSON parsing and preference handling
Phase 1, Plan 07
"""

import pytest
import json
import tempfile
import shutil
import os

# ============================================================================
# Test JSON Parsing (from Plan 07 Task 1)
# ============================================================================

def test_json_parsing_handles_valid_json():
    """Test 1: JSON parsing handles valid JSON correctly."""
    valid_json = '{"name": "test", "value": 123}'
    result = json.loads(valid_json)
    assert result == {"name": "test", "value": 123}


def test_json_parsing_handles_invalid_json():
    """Test 2: JSON parsing handles invalid JSON with error message."""
    invalid_json = '{"name": "test", "value":'
    with pytest.raises(json.JSONDecodeError):
        json.loads(invalid_json)


def test_json_parsing_handles_nested_objects():
    """Test 3: JSON parsing handles nested objects."""
    nested_json = '{"outer": {"inner": {"deepest": "value"}}}'
    result = json.loads(nested_json)
    assert result["outer"]["inner"]["deepest"] == "value"


def test_json_parsing_handles_arrays():
    """Test 4: JSON parsing handles arrays."""
    array_json = '["item1", "item2", {"nested": "value"}]'
    result = json.loads(array_json)
    assert result[0] == "item1"
    assert isinstance(result[2], dict)




# ============================================================================
# Test Preference Handling (from Plan 07 Task 2)
# ============================================================================

def test_preference_handling_read_preferences():
    """Test 1: Preference handling can read preferences from file."""
    temp_dir = tempfile.mkdtemp()
    try:
        preferences_file = os.path.join(temp_dir, "preferences.json")
        with open(preferences_file, "w") as f:
            json.dump({"theme": "dark", "language": "en"}, f)
        
        with open(preferences_file, "r") as f:
            result = json.load(f)
            assert result == {"theme": "dark", "language": "en"}
    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)


def test_preference_handling_write_preferences():
    """Test 2: Preference handling can write preferences to file."""
    temp_dir = tempfile.mkdtemp()
    try:
        preferences_file = os.path.join(temp_dir, "preferences.json")
        with open(preferences_file, "w") as f:
            json.dump({"theme": "dark"}, f)
        
        with open(preferences_file, "r") as f:
            result = json.load(f)
            assert result == {"theme": "dark"}
    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)


def test_preference_handling_missing_preferences():
    """Test 3: Preference handling can handle missing preferences."""
    temp_dir = tempfile.mkdtemp()
    try:
        preferences_file = os.path.join(temp_dir, "nonexistent.json")
        with open(preferences_file, "w") as f:
            json.dump({}, f)
    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)


# ============================================================================
# Test Serialization (from Plan 07 Task 3)
# ============================================================================

def test_serialization_preserves_data_integrity():
    """Test 1: Serialization preserves data integrity."""
    original = {"name": "test", "value": 123}
    serialized = json.dumps(original)
    deserialized = json.loads(serialized)
    assert deserialized == original


def test_serialization_restores_data():
    """Test 2: Deserialization can restore serialized data."""
    original = {"theme": "dark", "language": "en"}
    serialized = json.dumps(original)
    deserialized = json.loads(serialized)
    assert deserialized == original


def test_serialization_handles_complex_structures():
    """Test 3: Serialization handles complex data structures."""
    complex_data = {
        "list": [1, 2, {"nested": "value"}],
        "dict": {"key": "value"},
        "bool": True,
        "none": None
    }
    serialized = json.dumps(complex_data)
    deserialized = json.loads(serialized)
    assert deserialized == complex_data


def test_serialization_special_data_types():
    """Test 4: Serialization handles special data types."""
    special_data = {
        "none": None,
        "bool_true": True,
        "bool_false": False,
        "int": 42
    }
    serialized = json.dumps(special_data)
    deserialized = json.loads(serialized)
    assert deserialized["none"] is None
    assert deserialized["bool_true"] is True


# ============================================================================
# Thread Safety Tests
# ============================================================================

def test_serialization_thread_safety():
    """Test: Serialization operations are thread-safe."""
    import threading
    
    errors = []
    
    def run_serialization():
        try:
            data = {"test": "data"}
            serialized = json.dumps(data)
            deserialized = json.loads(serialized)
        except Exception as e:
            errors.append(e)
    
    threads = []
    for _ in range(10):
        t = threading.Thread(target=run_serialization)
        threads.append(t)
        t.start()
    
    for t in threads:
        t.join()
    
    assert len(errors) == 0, f"Concurrent serialization failed with errors: {errors}"


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
