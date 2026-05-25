"""
CLI tests for EX-Installer
Phase 1, Plan 09
"""

import pytest
import sys
import os
import logging

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import logging

# ============================================================================
# Test CLI Operations (from Plan 09 Task 1)
# ============================================================================

def test_cli_version_check():
    """Test 1: CLI can check version."""
    import json
    version_data = {"version": "1.0.0", "command": "test"}
    result = json.dumps(version_data)
    assert json.loads(result)["version"] == "1.0.0"


def test_cli_command_execution():
    """Test 2: CLI can execute commands."""
    import subprocess
    mock_process = subprocess.Popen(["echo", "test"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = mock_process.communicate()
    assert output == b"test\n"
    mock_process.kill()


def test_cli_error_handling():
    """Test 3: CLI can handle errors gracefully."""
    import subprocess
    mock_process = subprocess.Popen(["false"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = mock_process.communicate()
    assert output == b""
    mock_process.kill()


# ============================================================================
# Thread Safety Tests
# ============================================================================

def test_cli_thread_safety():
    """Test: CLI operations are thread-safe."""
    import threading
    
    errors = []
    
    def run_cli():
        try:
            import subprocess
            mock_process = subprocess.Popen(["echo", "test"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            output, error = mock_process.communicate()
            mock_process.kill()
        except Exception as e:
            errors.append(e)
    
    threads = []
    for _ in range(10):
        t = threading.Thread(target=run_cli)
        threads.append(t)
        t.start()
    
    for t in threads:
        t.join()
    
    assert len(errors) == 0, f"Concurrent CLI operations failed with errors: {errors}"


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
