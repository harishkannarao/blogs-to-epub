from dataclasses import dataclass
from pathlib import Path
from types import MappingProxyType

import pytest
from ebooklib import epub
import requests


@dataclass(frozen=True)
class ArgsKwArgsPair:
    args: tuple[any]
    kwargs: MappingProxyType[any]


@dataclass(frozen=True)
class MkdirCall:
    path: str
    argsPair: ArgsKwArgsPair


@pytest.fixture
def path_mkdir_fixture(monkeypatch) -> list[MkdirCall]:
    mkdir_calls: list[MkdirCall] = []

    def mock_mkdir(self: Path, *args: any, **kwargs: any):
        mkdir_calls.append(MkdirCall(str(self), ArgsKwArgsPair(tuple(args), MappingProxyType(kwargs))))
        return

    monkeypatch.setattr(Path, "mkdir", mock_mkdir)
    yield mkdir_calls


@dataclass(frozen=True)
class WriteEpubCall:
    name: str
    book: epub.EpubBook
    options: dict[any]


@pytest.fixture
def epub_write_fixture(monkeypatch) -> list[WriteEpubCall]:
    write_epub_calls: list[WriteEpubCall] = []

    def mock_write_epub(name: str, book: epub.EpubBook, options: dict[any] = None):
        write_epub_calls.append(WriteEpubCall(name, book, options))
        return

    monkeypatch.setattr(epub, "write_epub", mock_write_epub)
    yield write_epub_calls


@dataclass(frozen=True)
class MockGetResponse:
    response: any

    def json(self):
        return self.response


@dataclass(frozen=True)
class MockGetTextResponse:
    text: str


@pytest.fixture
def requests_get_fixture(monkeypatch) -> (list[ArgsKwArgsPair], list[MockGetResponse]):
    requests_get_calls: list[ArgsKwArgsPair] = []
    mock_get_responses: list[MockGetResponse] = []

    def mock_get(*args: any, **kwargs: any):
        requests_get_calls.append(ArgsKwArgsPair(tuple(args), MappingProxyType(kwargs)))
        if len(mock_get_responses) == 0:
            raise RuntimeError("response list is empty")
        resp = mock_get_responses[0]
        del mock_get_responses[0]
        return resp

    monkeypatch.setattr(requests, "get", mock_get)
    yield requests_get_calls, mock_get_responses
