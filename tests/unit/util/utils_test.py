from tests.unit.conftest import WriteEpubCall
from blog_to_epub.util.utils import write_to_epub
from ebooklib import epub
from assertpy import assert_that


def test__write_to_epub__creates_epub_book(
        epub_write_fixture: list[WriteEpubCall]):

    url = "http://example.com"
    write_to_epub("/tmp/path", "some-name", url, [])

    assert_that(epub_write_fixture).is_length(1)
    assert_that(epub_write_fixture[0].name).is_equal_to("/tmp/path/some-name.epub")
    assert_that(epub_write_fixture[0].options).is_equal_to({})
    result = epub_write_fixture[0].book
    assert_that(result.items).is_length(3)
    first_chapter: epub.EpubHtml = result.items[0]
    assert_that(first_chapter.content).contains("Url: " + url)
