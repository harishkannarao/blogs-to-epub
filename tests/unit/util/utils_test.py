from tests.unit.conftest import WriteEpubCall
from blog_to_epub.util.utils import write_to_epub


def test_write_to_epub(
        epub_write_fixture: list[WriteEpubCall]):

    write_to_epub("/tmp/path", "some-name", "http://example.com", [])

    assert len(epub_write_fixture) == 1
    assert epub_write_fixture[0].name == "/tmp/path/some-name.epub"
    assert epub_write_fixture[0].options == {}
