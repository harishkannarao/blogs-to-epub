from tests.unit.conftest import WriteEpubCall
from blog_to_epub.util.utils import write_to_epub
from ebooklib import epub
from assertpy import assert_that


def test__write_to_epub__creates_epub_book(
        epub_write_fixture: list[WriteEpubCall]):
    url = "http://example.com"
    output_dir = "/tmp/path"
    file_name = "some-name"
    first_chapter = epub.EpubHtml(title="first_chapter", file_name="first_chapter.xhtml", lang='en',
                                  content="first chapter content")
    second_chapter = epub.EpubHtml(title="second_chapter", file_name="second_chapter.xhtml", lang='en',
                                  content="second chapter content")

    write_to_epub(output_dir, file_name, url, [first_chapter, second_chapter])

    assert_that(epub_write_fixture).is_length(1)
    assert_that(epub_write_fixture[0].name).is_equal_to(output_dir + "/" + file_name + ".epub")
    assert_that(epub_write_fixture[0].options).is_equal_to({})
    result = epub_write_fixture[0].book
    assert_that(result.items).is_length(5)
    meta_chapter: epub.EpubHtml = result.items[0]
    assert_that(meta_chapter.content).contains("Url: " + url)
    assert_that(result.items[1]).is_same_as(first_chapter)
    assert_that(result.items[2]).is_same_as(second_chapter)
    assert_that(result.items[3]).is_instance_of(epub.EpubNcx)
    assert_that(result.items[4]).is_instance_of(epub.EpubNav)
