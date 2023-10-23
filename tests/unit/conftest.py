from dataclasses import dataclass

import pytest
from pathlib import Path
from ebooklib import epub
from types import MappingProxyType


@dataclass(frozen=True)
class MkdirCall:
    path: str
    args: tuple[any]
    kwargs: MappingProxyType[any]


@pytest.fixture
def path_mkdir_fixture(monkeypatch) -> list[MkdirCall]:
    mkdir_calls: list[MkdirCall] = []

    def mock_mkdir(self: Path, *args: any, **kwargs: any):
        mkdir_calls.append(MkdirCall(str(self), tuple(args), MappingProxyType(kwargs)))
        return

    monkeypatch.setattr(Path, "mkdir", mock_mkdir)
    yield mkdir_calls


@dataclass
class WriteEpubCall:
    name: str
    book: epub.EpubBook
    options: any


@pytest.fixture
def epub_write_fixture(monkeypatch) -> list[WriteEpubCall]:
    write_epub_calls: list[WriteEpubCall] = []

    def mock_write_epub(name: str, book: epub.EpubBook, options: any = None):
        write_epub_calls.append(WriteEpubCall(name, book, options))
        return

    monkeypatch.setattr(epub, "write_epub", mock_write_epub)
    yield write_epub_calls
