from dataclasses import dataclass

import pytest
from pathlib import Path


@dataclass
class MkdirCall:
    path: str
    kwargs: any


@pytest.fixture
def path_mkdir_fixture(monkeypatch) -> list[MkdirCall]:
    mkdir_calls: list[MkdirCall] = []

    def mock_mkdir(self: Path, *args, **kwargs: any):
        mkdir_calls.append(MkdirCall(str(self), kwargs))
        return

    monkeypatch.setattr(Path, "mkdir", mock_mkdir)
    yield mkdir_calls
