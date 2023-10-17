from pathlib import Path


def create_path(output_dir):
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    return


def test_path_mocking(path_mkdir_fixture):
    create_path("/abc")
    assert len(path_mkdir_fixture) == 1
    assert path_mkdir_fixture[0]['path'] == '/abc'
    assert path_mkdir_fixture[0]['kwargs']['parents'] is True
    assert path_mkdir_fixture[0]['kwargs']['exist_ok'] is True
