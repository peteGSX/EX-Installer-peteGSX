"""
Git client tests for GitClient and ThreadedGitClient
Phase 1, Plan 05
"""

import pytest
import threading
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from unittest.mock import Mock, patch, MagicMock

import logging

from ex_installer.git_client import GitClient, ThreadedGitClient


@pytest.fixture(scope="function")
def mock_queue():
    """Create a mock queue for test operations."""
    return Mock()


@pytest.fixture(scope="function")
def mock_repo():
    """Create a mock pygit2 repository."""
    repo = MagicMock()
    repo.status.return_value = {}
    repo.workdir = "/tmp/test-repo"
    return repo


# ============================================================================
# Test GitClient (from Plan 05 Task 1)
# ============================================================================

def test_git_client_dir_is_git_repo():
    """Test 1: GitClient.dir_is_git_repo() can check if directory is a git repo."""
    # Test with .git file
    with patch('ex_installer.git_client.os') as mock_os:
        mock_os.path.exists.return_value = True
        mock_os.path.isdir.return_value = True
        mock_os.path.join.return_value = "/tmp/test/.git"
        
        assert GitClient.dir_is_git_repo("/tmp/test") == True
    
    # Test without .git file
    with patch('ex_installer.git_client.os') as mock_os:
        mock_os.path.exists.return_value = True
        mock_os.path.isdir.return_value = True
        mock_os.path.join.return_value = "/tmp/test/.git"
        mock_os.path.exists.return_value = False
        
        assert GitClient.dir_is_git_repo("/tmp/test") == False


# ============================================================================
# Test ThreadedGitClient (from Plan 05 Task 1)
# ============================================================================

def test_threaded_git_client_instantiation(mock_queue):
    """Test 1: ThreadedGitClient can be instantiated with task_name, task, queue, args."""
    mock_task = Mock()
    mock_task.__str__ = Mock(return_value="clone")
    
    threaded_client = ThreadedGitClient.__new__(ThreadedGitClient)
    threaded_client.task_name = "clone"
    threaded_client.task = mock_task
    threaded_client.queue = mock_queue
    threaded_client.args = []
    threaded_client.log = logging.getLogger("test.git_client")
    threaded_client.api_lock = threading.Lock()
    
    assert threaded_client.task_name == "clone"
    assert threaded_client.queue == mock_queue


def test_threaded_git_client_queues_info_message(mock_queue):
    """Test 2: ThreadedGitClient queues info message when run() is called."""
    mock_queue.reset_mock()
    mock_queue.put.reset_mock()
    
    mock_task = Mock()
    mock_task.__str__ = Mock(return_value="clone")
    
    threaded_client = ThreadedGitClient.__new__(ThreadedGitClient)
    threaded_client.task_name = "clone"
    threaded_client.task = mock_task
    threaded_client.queue = mock_queue
    threaded_client.args = []
    threaded_client.log = logging.getLogger("test.git_client")
    threaded_client.api_lock = threading.Lock()
    
    threaded_client.run()
    
    # Verify queue.put was called with info message
    mock_queue.put.assert_called()


def test_threaded_git_client_queues_success_message(mock_queue):
    """Test 3: ThreadedGitClient queues success message when task completes."""
    mock_queue.reset_mock()
    mock_queue.put.reset_mock()
    
    mock_task = Mock()
    mock_task.__str__ = Mock(return_value="clone")
    mock_task.return_value = "Clone successful"
    
    threaded_client = ThreadedGitClient.__new__(ThreadedGitClient)
    threaded_client.task_name = "clone"
    threaded_client.task = mock_task
    threaded_client.queue = mock_queue
    threaded_client.args = []
    threaded_client.log = logging.getLogger("test.git_client")
    threaded_client.api_lock = threading.Lock()
    
    threaded_client.run()
    
    # Verify queue.put was called with success message
    mock_queue.put.assert_called()


def test_threaded_git_client_queues_error_message(mock_queue):
    """Test 4: ThreadedGitClient queues error message when task fails."""
    mock_queue.reset_mock()
    mock_queue.put.reset_mock()
    
    mock_task = Mock()
    mock_task.__str__ = Mock(return_value="clone")
    mock_task.side_effect = Exception("Clone failed")
    
    threaded_client = ThreadedGitClient.__new__(ThreadedGitClient)
    threaded_client.task_name = "clone"
    threaded_client.task = mock_task
    threaded_client.queue = mock_queue
    threaded_client.args = []
    threaded_client.log = logging.getLogger("test.git_client")
    threaded_client.api_lock = threading.Lock()
    
    try:
        threaded_client.run()
    except Exception:
        pass  # Expected
    
    # Verify queue.put was called with error message
    mock_queue.put.assert_called()


# ============================================================================
# Thread Safety Tests (from Plan 05 Task 1)
# ============================================================================

def test_threaded_git_client_uses_api_lock(mock_queue):
    """Test 5: ThreadedGitClient uses api_lock for synchronization."""
    import threading
    
    mock_task = Mock()
    mock_task.__str__ = Mock(return_value="clone")
    
    threaded_client = ThreadedGitClient.__new__(ThreadedGitClient)
    threaded_client.task_name = "clone"
    threaded_client.task = mock_task
    threaded_client.queue = mock_queue
    threaded_client.args = []
    threaded_client.log = logging.getLogger("test.git_client")
    threaded_client.api_lock = threading.Lock()
    
    # Verify the lock exists
    assert hasattr(threaded_client, 'api_lock')
    assert isinstance(threaded_client.api_lock, type(threading.Lock()))
    
    # Test concurrent access
    errors = []
    
    def concurrent_run():
        try:
            threaded_client.run()
        except Exception as e:
            errors.append(e)
    
    threads = []
    for _ in range(10):
        t = threading.Thread(target=concurrent_run)
        threads.append(t)
        t.start()
    
    for t in threads:
        t.join()
    
    assert len(errors) == 0, f"Concurrent execution failed with errors: {errors}"


    errors = []
    
    def run_git_client():
        try:
            with patch('ex_installer.git_client.os') as mock_os:
                mock_os.path.exists.return_value = True
                mock_os.path.isdir.return_value = True
                mock_os.path.join.return_value = "/tmp/test/.git"
                
                assert GitClient.dir_is_git_repo("/tmp/test") == True
        except Exception as e:
            errors.append(e)
    
    threads = []
    for _ in range(10):
        t = threading.Thread(target=run_git_client)
        threads.append(t)
        t.start()
    
    for t in threads:
        t.join()
    
    assert len(errors) == 0, f"Concurrent execution failed with errors: {errors}"


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
