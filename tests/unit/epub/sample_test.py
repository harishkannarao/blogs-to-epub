from pathlib import Path
from tests.unit.conftest import MkdirCall


def create_path(output_dir):
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    return


def test_path_mocking(path_mkdir_fixture: list[MkdirCall]):
    create_path("/abc")
    assert len(path_mkdir_fixture) == 1
    assert path_mkdir_fixture[0].path == '/abc'
    assert path_mkdir_fixture[0].kwargs['parents'] is True
    assert path_mkdir_fixture[0].kwargs['exist_ok'] is True
