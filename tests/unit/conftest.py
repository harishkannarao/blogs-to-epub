import pytest
from pathlib import Path


@pytest.fixture
def path_mkdir_fixture(monkeypatch):
    mkdir_calls = []

    def mock_mkdir(self: Path, *args, **kwargs):
        mkdir_calls.append({'path': str(self), 'kwargs': kwargs})
        return

    monkeypatch.setattr(Path, "mkdir", mock_mkdir)
    yield mkdir_calls
