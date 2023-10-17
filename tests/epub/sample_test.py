from pathlib import Path
import pytest


@pytest.fixture
def path_mkdir_fixture(monkeypatch):
    mkdir_calls = []

    def mock_mkdir(self: Path, *args, **kwargs):
        mkdir_calls.append({'path': str(self), 'kwargs': kwargs})
        return

    monkeypatch.setattr(Path, "mkdir", mock_mkdir)
    yield mkdir_calls


def create_path(output_dir):
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    return


def test_path_mocking(path_mkdir_fixture):
    create_path("/abc")
    assert len(path_mkdir_fixture) == 1
    assert path_mkdir_fixture[0]['path'] == '/abc'
    assert path_mkdir_fixture[0]['kwargs']['parents'] is True
    assert path_mkdir_fixture[0]['kwargs']['exist_ok'] is True
