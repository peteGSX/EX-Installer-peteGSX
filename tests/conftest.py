"""Pytest configuration and fixtures for test infrastructure."""



# ============================================================================
# Mock Arduino Devices
# ============================================================================

class MockArduino:
    """Mock Arduino device for testing ArduinoCLI interactions."""
    
    def __init__(self, device_id: str = "MOCK_DEVICE_001", firmware_version: str = "1.0.0"):
        self.device_id = device_id
        self.firmware_version = firmware_version
        self.last_command = None
    
    def upload_firmware(self, firmware: str, timeout: int = 10) -> bool:
        """Simulate firmware upload."""
        self.last_command = "upload"
        return True
    
    def flash_firmware(self, firmware: str, timeout: int = 10) -> bool:
        """Simulate firmware flashing."""
        self.last_command = "flash"
        return True


@pytest.fixture(scope="function")
def mock_device():
    """Create a mock Arduino device for testing."""
    return MockArduino()


# ============================================================================
# Mock GitHub Releases
# ============================================================================

class MockGitHubRelease:
    """Mock GitHub release for testing GitClient interactions."""
    
    def __init__(
        self,
        tag_name: str,
        assets: list,
        release_url: str,
        releases_url: str,
        version: str = "v1.0.0",
        prerelease: bool = False,
        published_at: str = "2024-01-01T00:00:00Z"
    ):
        self.tag_name = tag_name
        self.assets = assets
        self.release_url = release_url
        self.releases_url = releases_url
        self.version = version
        self.prerelease = prerelease
        self.published_at = published_at
    
    def get_asset(self, name: str) -> str:
        """Get asset URL."""
        return f"https://github.com/test/repo/releases/download/{self.tag_name}/{name}"


@pytest.fixture(scope="function")
def mock_github_release():
    """Create a mock GitHub release for testing."""
    return MockGitHubRelease(
        tag_name="v1.0.0",
        assets=[],
        release_url="https://api.github.com/repos/test/repo/releases/1",
        releases_url="https://github.com/test/repo/releases"
    )


# ============================================================================
# Mock Serial Communication
# ============================================================================

class MockSerial:
    """Mock serial device for testing serial_monitor interactions."""
    
    def __init__(self, buffer: bytes = b""):
        self.buffer = buffer
        self.read_count = 0
    
    def write(self, data: bytes) -> int:
        """Write data to serial buffer."""
        self.buffer = data
        return len(data)
    
    def read(self, count: int = -1) -> bytes:
        """Read data from serial buffer."""
        if count == -1:
            data = self.buffer
        else:
            data = self.buffer[:count]
        self.buffer = b""
        self.read_count += 1
        return data


@pytest.fixture(scope="function")
def mock_serial():
    """Create a mock serial device for testing."""
    return MockSerial()


# ============================================================================
# Synthetic Error Conditions
# ============================================================================

class NetworkError(Exception):
    """Synthetic network error for testing."""
    
    def __init__(self, message: str = "Network error", timeout: int = 30):
        self.message = message
        self.timeout = timeout
    
    def __str__(self):
        return f"Network error ({self.message})"


class DiskFullError(Exception):
    """Synthetic disk full error for testing."""
    
    def __init__(self, available_bytes: int = 0):
        self.available_bytes = available_bytes
    
    def __str__(self):
        return f"Disk full: {self.available_bytes} bytes available"


@pytest.fixture
def network_error():
    """Create a synthetic network error for testing."""
    return NetworkError("timeout")


@pytest.fixture
def disk_full_error():
    """Create a synthetic disk full error for testing."""
    return DiskFullError(0)


