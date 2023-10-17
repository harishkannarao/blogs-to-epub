from pathlib import Path


def getssh():
    """Simple function to return expanded homedir ssh path."""
    return Path.home() / ".ssh"


def create_path(output_dir):
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    return


def test_sample(monkeypatch):
    # mocked return function to replace Path.home
    # always return '/abc'
    def mockreturn():
        return Path("/abc")

    # Application of the monkeypatch to replace Path.home
    # with the behavior of mockreturn defined above.
    monkeypatch.setattr(Path, "home", mockreturn)

    x = getssh()
    assert x == Path("/abc/.ssh")


def test_sample2(monkeypatch):
    mkdir_calls = []

    def mock_mkdir(self: Path, *args, **kwargs):
        mkdir_calls.append({'path': str(self), 'kwargs': kwargs})
        return

    monkeypatch.setattr(Path, "mkdir", mock_mkdir)

    create_path("/abc")
    assert len(mkdir_calls) == 1
    assert mkdir_calls[0]['path'] == '/abc'
    assert mkdir_calls[0]['kwargs']['parents'] is True
    assert mkdir_calls[0]['kwargs']['exist_ok'] is True
