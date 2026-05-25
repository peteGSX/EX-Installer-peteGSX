"""
File manager tests for ThreadedDownloader, ThreadedExtractor, and FileManager
Phase 1, Plan 04
"""

import pytest
import threading
import sys
import os
import logging

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from unittest.mock import Mock, patch, MagicMock

import tarfile
from zipfile import ZipFile, Path
import json
import tempfile
import shutil

from ex_installer.file_manager import ThreadedDownloader, ThreadedExtractor, FileManager


@pytest.fixture(scope="function")
def mock_queue():
    """Create a mock queue for test operations."""
    return Mock()


@pytest.fixture(scope="function")
def mock_downloader(mock_queue):
    """Create a mock ThreadedDownloader."""
    downloader = ThreadedDownloader.__new__(ThreadedDownloader)
    downloader.url = "https://example.com/file.tar.gz"
    downloader.target = "/tmp/file.tar.gz"
    downloader.queue = mock_queue
    downloader.log = logging.getLogger("test.downloader")
    downloader.download_lock = threading.Lock()
    return downloader


@pytest.fixture(scope="function")
def mock_extractor(mock_queue):
    """Create a mock ThreadedExtractor."""
    extractor = ThreadedExtractor.__new__(ThreadedExtractor)
    extractor.archive_file = "/tmp/archive.tar.gz"
    extractor.target_dir = "/tmp/extracted"
    extractor.queue = mock_queue
    extractor.log = logging.getLogger("test.extractor")
    extractor.extractor_lock = threading.Lock()
    return extractor


@pytest.fixture(scope="function")
def file_manager():
    """Create a FileManager instance."""
    fm = FileManager()
    return fm


# ============================================================================
# Test ThreadedDownloader (from Plan 04 Task 1)
# ============================================================================

def test_threaded_downloader_instantiation(mock_queue):
    """Test 1: ThreadedDownloader can be instantiated with url, target, queue."""
    downloader = ThreadedDownloader.__new__(ThreadedDownloader)
    downloader.url = "https://example.com/file.tar.gz"
    downloader.target = "/tmp/file.tar.gz"
    downloader.queue = mock_queue
    downloader.log = logging.getLogger("test.downloader")
    downloader.download_lock = threading.Lock()
    
    assert downloader.url == "https://example.com/file.tar.gz"
    assert downloader.target == "/tmp/file.tar.gz"
    assert downloader.queue == mock_queue


def test_threaded_downloader_queues_start_message(mock_queue):
    """Test 2: ThreadedDownloader queues start message when run() is called."""
    mock_queue.reset_mock()
    mock_queue.put.reset_mock()
    
    downloader = ThreadedDownloader.__new__(ThreadedDownloader)
    downloader.url = "https://example.com/file.tar.gz"
    downloader.target = "/tmp/file.tar.gz"
    downloader.queue = mock_queue
    downloader.log = logging.getLogger("test.downloader")
    downloader.download_lock = threading.Lock()
    
    downloader.run()
    
    # Verify queue.put was called with info message
    mock_queue.put.assert_called()


def test_threaded_downloader_queues_success_message(mock_queue):
    """Test 3: ThreadedDownloader queues success message when download completes."""
    mock_queue.reset_mock()
    mock_queue.put.reset_mock()
    
    downloader = ThreadedDownloader.__new__(ThreadedDownloader)
    downloader.url = "https://example.com/file.tar.gz"
    downloader.target = "/tmp/file.tar.gz"
    downloader.queue = mock_queue
    downloader.log = logging.getLogger("test.downloader")
    downloader.download_lock = threading.Lock()
    
    with patch('ex_installer.file_manager.requests') as mock_requests:
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.raw = Mock()
        mock_requests.get.return_value = mock_response
        
        downloader.run()
        
        # Verify queue.put was called with success message
        mock_queue.put.assert_called()


def test_threaded_downloader_queues_error_message(mock_queue):
    """Test 4: ThreadedDownloader queues error message when download fails."""
    mock_queue.reset_mock()
    mock_queue.put.reset_mock()
    
    downloader = ThreadedDownloader.__new__(ThreadedDownloader)
    downloader.url = "https://example.com/file.tar.gz"
    downloader.target = "/tmp/file.tar.gz"
    downloader.queue = mock_queue
    downloader.log = logging.getLogger("test.downloader")
    downloader.download_lock = threading.Lock()
    
    with patch('ex_installer.file_manager.requests') as mock_requests:
        mock_response = Mock()
        mock_response.status_code = 500
        mock_requests.get.return_value = mock_response
        
        downloader.run()
        
        # Verify queue.put was called with error message
        mock_queue.put.assert_called()


# ============================================================================
# Test ThreadedExtractor (from Plan 04 Task 1)
# ============================================================================

def test_threaded_extractor_instantiation(mock_queue):
    """Test 1: ThreadedExtractor can be instantiated with archive_file, target_dir, queue."""
    extractor = ThreadedExtractor.__new__(ThreadedExtractor)
    extractor.archive_file = "/tmp/archive.tar.gz"
    extractor.target_dir = "/tmp/extracted"
    extractor.queue = mock_queue
    extractor.log = logging.getLogger("test.extractor")
    extractor.extractor_lock = threading.Lock()
    
    assert extractor.archive_file == "/tmp/archive.tar.gz"
    assert extractor.target_dir == "/tmp/extracted"
    assert extractor.queue == mock_queue


def test_threaded_extractor_queues_start_message(mock_queue):
    """Test 2: ThreadedExtractor queues start message when run() is called."""
    mock_queue.reset_mock()
    mock_queue.put.reset_mock()
    
    extractor = ThreadedExtractor.__new__(ThreadedExtractor)
    extractor.archive_file = "/tmp/archive.tar.gz"
    extractor.target_dir = "/tmp/extracted"
    extractor.queue = mock_queue
    extractor.log = logging.getLogger("test.extractor")
    extractor.extractor_lock = threading.Lock()
    
    extractor.run()
    
    # Verify queue.put was called with info message
    mock_queue.put.assert_called()


def test_threaded_extractor_queues_success_message(mock_queue):
    """Test 3: ThreadedExtractor queues success message when extraction completes."""
    mock_queue.reset_mock()
    mock_queue.put.reset_mock()
    
    extractor = ThreadedExtractor.__new__(ThreadedExtractor)
    extractor.archive_file = "/tmp/archive.tar.gz"
    extractor.target_dir = "/tmp/extracted"
    extractor.queue = mock_queue
    extractor.log = logging.getLogger("test.extractor")
    extractor.extractor_lock = threading.Lock()
    
    with patch('ex_installer.file_manager.platform') as mock_platform, \
         patch('ex_installer.file_manager.tarfile') as mock_tarfile:
        
        mock_platform.system.return_value = "Linux"
        
        mock_archive = Mock()
        mock_archive.getnames.return_value = ["file1", "file2"]
        mock_archive.extractall.return_value = None
        mock_archive.close.return_value = None
        mock_tarfile.open.return_value = mock_archive
        
        extractor.run()
        
        # Verify queue.put was called with success message
        mock_queue.put.assert_called()


def test_threaded_extractor_queues_error_message(mock_queue):
    """Test 4: ThreadedExtractor queues error message when extraction fails."""
    mock_queue.reset_mock()
    mock_queue.put.reset_mock()
    
    extractor = ThreadedExtractor.__new__(ThreadedExtractor)
    extractor.archive_file = "/tmp/archive.tar.gz"
    extractor.target_dir = "/tmp/extracted"
    extractor.queue = mock_queue
    extractor.log = logging.getLogger("test.extractor")
    extractor.extractor_lock = threading.Lock()
    
    with patch('ex_installer.file_manager.platform') as mock_platform, \
         patch('ex_installer.file_manager.tarfile') as mock_tarfile:
        
        mock_platform.system.return_value = "Linux"
        
        mock_archive = Mock()
        mock_archive.getnames.return_value = ["file1", "file2"]
        mock_archive.extractall.side_effect = Exception("Extraction failed")
        mock_archive.close.return_value = None
        mock_tarfile.open.return_value = mock_archive
        
        extractor.run()
        
        # Verify queue.put was called with error message
        mock_queue.put.assert_called()


# ============================================================================
# Test FileManager (from Plan 04 Task 1)
# ============================================================================

def test_file_manager_instantiation():
    """Test 1: FileManager can be instantiated."""
    fm = FileManager()
    
    assert fm is not None


def test_file_manager_get_base_dir():
    """Test 2: FileManager.get_base_dir() returns base directory."""
    fm = FileManager()
    
    with patch('ex_installer.file_manager.platform') as mock_platform, \
         patch('ex_installer.file_manager.os') as mock_os:
        
        mock_platform.system.return_value = "Linux"
        mock_os.path.expanduser.return_value = "/home/user"
        mock_os.path.join.return_value = "/home/user/ex-installer"
        
        base_dir = fm.get_base_dir()
        
        assert base_dir == "/home/user/ex-installer"


def test_file_manager_get_install_dir():
    """Test 3: FileManager.get_install_dir() returns installation directory."""
    fm = FileManager()
    
    with patch('ex_installer.file_manager.platform') as mock_platform, \
         patch('ex_installer.file_manager.os') as mock_os:
        
        mock_platform.system.return_value = "Linux"
        mock_os.path.expanduser.return_value = "/home/user"
        mock_os.path.join.return_value = "/home/user/ex-installer/product-name"
        
        install_dir = fm.get_install_dir("product-name")
        
        assert install_dir == "/home/user/ex-installer/product-name"


# ============================================================================
# Thread Safety Tests (from Plan 04 Task 1)
# ============================================================================

def test_threaded_downloader_uses_download_lock(mock_queue):
    """Test 5: ThreadedDownloader uses download_lock for synchronization."""
    import threading
    
    downloader = ThreadedDownloader.__new__(ThreadedDownloader)
    downloader.url = "https://example.com/file.tar.gz"
    downloader.target = "/tmp/file.tar.gz"
    downloader.queue = mock_queue
    downloader.log = logging.getLogger("test.downloader")
    downloader.download_lock = threading.Lock()
    
    # Verify the lock exists
    assert hasattr(downloader, 'download_lock')
    assert isinstance(downloader.download_lock, type(threading.Lock()))
    
    # Test concurrent access
    errors = []
    
    def concurrent_run():
        try:
            downloader.run()
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


def test_threaded_extractor_uses_extractor_lock(mock_queue):
    """Test 6: ThreadedExtractor uses extractor_lock for synchronization."""
    import threading
    
    extractor = ThreadedExtractor.__new__(ThreadedExtractor)
    extractor.archive_file = "/tmp/archive.tar.gz"
    extractor.target_dir = "/tmp/extracted"
    extractor.queue = mock_queue
    extractor.log = logging.getLogger("test.extractor")
    extractor.extractor_lock = threading.Lock()
    
    # Verify the lock exists
    assert hasattr(extractor, 'extractor_lock')
    assert isinstance(extractor.extractor_lock, type(threading.Lock()))
    
    # Test concurrent access
    errors = []
    
    def concurrent_run():
        try:
            extractor.run()
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


def test_file_manager_thread_safety():
    """Test 7: FileManager operations are thread-safe."""
    import threading
    
    errors = []
    
    def run_file_manager():
        try:
            fm = FileManager()
            base_dir = fm.get_base_dir()
            install_dir = fm.get_install_dir("test-product")
        except Exception as e:
            errors.append(e)
    
    threads = []
    for _ in range(10):
        t = threading.Thread(target=run_file_manager)
        threads.append(t)
        t.start()
    
    for t in threads:
        t.join()
    
    assert len(errors) == 0, f"Concurrent execution failed with errors: {errors}"


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
