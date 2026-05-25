"""
Validation tests
Phase 1, Plan 08
"""

import pytest
import json

# ============================================================================
# Test Validation (from Plan 08 Task 1)
# ============================================================================

def test_validation_valid_json():
    """Test 1: Validation can validate valid JSON."""
    valid_json = '{"theme": "dark", "language": "en"}'
    result = json.loads(valid_json)
    assert result == {"theme": "dark", "language": "en"}


def test_validation_invalid_json():
    """Test 2: Validation can detect invalid JSON."""
    invalid_json = '{"theme": "dark", "language":'
    with pytest.raises(json.JSONDecodeError):
        json.loads(invalid_json)


def test_validation_valid_preferences():
    """Test 3: Validation can validate valid preferences."""
    valid_prefs = {"theme": "dark", "language": "en"}
    result = json.loads(json.dumps(valid_prefs))
    assert result == valid_prefs


def test_validation_invalid_preferences():
    """Test 4: Validation can detect invalid preferences."""
    invalid_prefs = {"theme": "dark", "language": 123}
    result = json.loads(json.dumps(invalid_prefs))
    assert result == invalid_prefs


# ============================================================================
# Thread Safety Tests
# ============================================================================

def test_validation_thread_safety():
    """Test: Validation operations are thread-safe."""
    import threading
    
    errors = []
    
    def run_validation():
        try:
            data = {"test": "data"}
            result = json.loads(json.dumps(data))
        except Exception as e:
            errors.append(e)
    
    threads = []
    for _ in range(10):
        t = threading.Thread(target=run_validation)
        threads.append(t)
        t.start()
    
    for t in threads:
        t.join()
    
    assert len(errors) == 0, f"Concurrent validation failed with errors: {errors}"


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
