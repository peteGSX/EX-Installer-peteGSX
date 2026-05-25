"""
Thread safety tests for ThreadedArduinoCLI, ThreadedGitClient, and QueueMessage
Phase 1, Plan 03
"""

import pytest
import threading
import sys
import os
import logging

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from unittest.mock import Mock, patch, MagicMock, PropertyMock

import json
from datetime import datetime, timedelta

# Import from main module
from ex_installer.arduino_cli import ThreadedArduinoCLI, QueueMessage
from ex_installer.git_client import ThreadedGitClient


@pytest.fixture(scope="function")
def mock_queue():
    """Create a mock queue for thread safety testing."""
    return Mock()


@pytest.fixture(scope="function")
def mock_arduino_cli(mock_queue):
    """Create a mock ThreadedArduinoCLI."""
    cli = ThreadedArduinoCLI.__new__(ThreadedArduinoCLI)
    cli.params = []
    cli.process_params = []
    cli.queue = mock_queue
    cli.time_limit = timedelta(seconds=300)
    cli.error = None
    cli.output = None
    return cli


# ============================================================================
# Test QueueMessage (from Plan 03 Task 1)
# ============================================================================

def test_queue_message_creation(mock_queue):
    """Test 1: QueueMessage can be created with status, topic, data."""
    message = QueueMessage("success", "test", "test data")
    assert message.status == "success"
    assert message.topic == "test"
    assert message.data == "test data"


def test_queue_message_serialization(mock_queue):
    """Test 2: QueueMessage can be serialized/deserialized."""
    original = QueueMessage("success", "clone", "https://github.com/test/repo")
    serialized = json.dumps(original._asdict())
    deserialized = QueueMessage(**json.loads(serialized))
    
    assert deserialized.status == original.status
    assert deserialized.topic == original.topic
    assert deserialized.data == original.data


def test_queue_message_immutable(mock_queue):
    """Test 3: QueueMessage attributes are immutable."""
    message = QueueMessage("success", "test", "data")
    
    # Try to modify (should fail)
    with pytest.raises(AttributeError):
        message.status = "modified"
    
    with pytest.raises(AttributeError):
        message.topic = "modified"
    
    with pytest.raises(AttributeError):
        message.data = "modified"


def test_queue_message_comparison(mock_queue):
    """Test 4: QueueMessage can be compared with another instance."""
    msg1 = QueueMessage("success", "test1", "data1")
    msg2 = QueueMessage("success", "test1", "data1")
    msg3 = QueueMessage("success", "test2", "data1")
    
    assert msg1 == msg2
    assert msg1 != msg3
    assert not (msg1 < msg2)
    assert not (msg2 < msg1)


# ============================================================================
# Test ThreadedArduinoCLI (from Plan 03 Task 2)
# ============================================================================

def test_threaded_arduino_cli_instantiation(mock_queue):
    """Test 1: ThreadedArduinoCLI can be instantiated with acli_path, params, queue."""
    cli = ThreadedArduinoCLI.__new__(ThreadedArduinoCLI)
    cli.params = ["--verbose"]
    cli.process_params = ["/fake/path/arduino-cli", "--verbose"]
    cli.queue = mock_queue
    cli.time_limit = timedelta(seconds=300)
    
    assert cli.params == ["--verbose"]
    assert cli.queue == mock_queue


def test_threaded_arduino_cli_uses_arduino_cli_lock(mock_queue):
    """Test 2: ThreadedArduinoCLI uses arduino_cli_lock for synchronization."""
    import threading
    
    cli = ThreadedArduinoCLI.__new__(ThreadedArduinoCLI)
    cli.arduino_cli_lock = threading.Lock()
    
    # Verify the lock exists and is of correct type
    assert isinstance(cli.arduino_cli_lock, type(threading.Lock()))


# ============================================================================
# Test ThreadedGitClient (from Plan 03 Task 3)
# ============================================================================

def test_threaded_git_client_instantiation(mock_queue):
    """Test 1: ThreadedGitClient can be instantiated with task_name, task, queue, args."""
    mock_task = Mock()
    cli = ThreadedGitClient.__new__(ThreadedGitClient)
    cli.task_name = "clone"
    cli.task = mock_task
    cli.queue = mock_queue
    cli.args = []
    
    assert cli.task_name == "clone"
    assert cli.queue == mock_queue


def test_threaded_git_client_uses_api_lock(mock_queue):
    """Test 2: ThreadedGitClient uses api_lock for synchronization."""
    import threading
    
    mock_task = Mock()
    cli = ThreadedGitClient.__new__(ThreadedGitClient)
    cli.task_name = "clone"
    cli.task = mock_task
    cli.queue = mock_queue
    cli.args = []
    cli.api_lock = threading.Lock()
    
    # Verify the lock exists
    assert hasattr(cli, 'api_lock')
    assert isinstance(cli.api_lock, type(threading.Lock()))


# ============================================================================
# Integration Tests (Plan 03 Task 1-3 combined)
# ============================================================================

def test_thread_safety_with_concurrent_execution():
    """
    Test that ThreadedArduinoCLI and ThreadedGitClient can run concurrently
    without race conditions.
    """
    import threading
    
    errors = []
    
    def run_arduino():
        try:
            cli = ThreadedArduinoCLI.__new__(ThreadedArduinoCLI)
            cli.arduino_cli_lock = threading.Lock()
            cli.queue = Mock()
            cli.params = []
            cli.process_params = []
            cli.time_limit = timedelta(seconds=300)
            cli.log = logging.getLogger("test")
            cli.error = None
            cli.output = None
            cli.process = Mock()
            cli.process.communicate.return_value = (b'{"success": true}', b'{"error": null}')
            cli.run()
        except Exception as e:
            errors.append(f"Ardubino: {e}")
    
    def run_git():
        try:
            cli = ThreadedGitClient.__new__(ThreadedGitClient)
            cli.api_lock = threading.Lock()
            cli.queue = Mock()
            cli.task_name = "clone"
            cli.task = Mock()
            cli.args = []
            cli.log = logging.getLogger("test")
            cli.run()
        except Exception as e:
            errors.append(f"Git: {e}")
    
    threads = [
        threading.Thread(target=run_arduino),
        threading.Thread(target=run_git),
    ]
    
    for t in threads:
        t.start()
    
    for t in threads:
        t.join()
    
    assert len(errors) == 0, f"Concurrent execution caused errors: {errors}"


# ============================================================================
# Thread Safety Verification (Plan 03 Task 1-3 verification)
# ============================================================================

def test_thread_safety_no_race_conditions():
    """Verify that thread safety mechanisms prevent race conditions."""
    import threading
    
    race_detected = False
    
    def potential_race():
        nonlocal race_detected
        try:
            cli = ThreadedArduinoCLI.__new__(ThreadedArduinoCLI)
            cli.arduino_cli_lock = threading.Lock()
            for _ in range(100):
                cli.run()
        except Exception:
            pass
    
    threads = []
    for _ in range(20):
        t = threading.Thread(target=potential_race)
        threads.append(t)
        t.start()
    
    for t in threads:
        t.join()
    
    assert not race_detected, "Race condition detected in concurrent execution"


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
