from pathlib import Path
from tests.unit.conftest import MkdirCall


def create_path(output_dir):
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    return


def test_path_mocking(path_mkdir_fixture: list[MkdirCall]):
    create_path("/abc")
    assert len(path_mkdir_fixture) == 1
    assert path_mkdir_fixture[0].path == '/abc'
    assert len(path_mkdir_fixture[0].argsPair.args) == 0
    assert path_mkdir_fixture[0].argsPair.kwargs.get('parents') is True
    assert path_mkdir_fixture[0].argsPair.kwargs.get('exist_ok') is True
