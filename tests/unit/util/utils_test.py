from assertpy import assert_that
from ebooklib import epub

from blog_to_epub.util.utils import write_to_epub
from blog_to_epub.util.utils import get_all_urls
from blog_to_epub.util.utils import get_all_chapters
from tests.unit.conftest import WriteEpubCall, RequestsGetCall, MockGetResponse
from tests.unit.response.response_generator import create_blog_response


def test__write_to_epub__creates_epub_book(
        epub_write_fixture: list[WriteEpubCall]
):
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


def test__get_all_urls__returns_all_urls__from_initial_url(
        requests_get_fixture: (list[RequestsGetCall], list[MockGetResponse])
):
    get_calls: list[RequestsGetCall] = requests_get_fixture[0]
    get_mock_responses: list[MockGetResponse] = requests_get_fixture[1]

    get_mock_responses.extend([
        create_blog_response(next_link='http://example.com?page=2'),
        create_blog_response(next_link='http://example.com?page=3'),
        create_blog_response(next_link=None),
    ])

    initial_url: str = 'http://example.com'
    result: list[str] = get_all_urls(initial_url)

    assert_that(result).is_length(3)
    assert_that(result[0]).is_equal_to('http://example.com')
    assert_that(result[1]).is_equal_to('http://example.com?page=2')
    assert_that(result[2]).is_equal_to('http://example.com?page=3')

    assert_that(get_calls).is_length(3)
    assert_that(get_calls[0].args[0]).is_equal_to('http://example.com')
    assert_that(get_calls[1].args[0]).is_equal_to('http://example.com?page=2')
    assert_that(get_calls[2].args[0]).is_equal_to('http://example.com?page=3')


def test__get_all_chapters__returns_all_chapters_from_urls(
        requests_get_fixture: (list[RequestsGetCall], list[MockGetResponse])
):
    get_calls: list[RequestsGetCall] = requests_get_fixture[0]
    get_mock_responses: list[MockGetResponse] = requests_get_fixture[1]

    get_mock_responses.extend([
        create_blog_response(chapters=[
            ('title 2', 'chapter 2'),
            ('title 1', 'chapter 1'),
        ]),
        create_blog_response(chapters=[
            ('title 4', 'chapter 4'),
            ('title 3', 'chapter 3'),
        ]),
    ])

    result = get_all_chapters(['http://example.com', 'http://example.com?page=2'])

    assert_that(result).is_length(4)

    assert_that(result[0].title).is_equal_to('title 1')
    assert_that(result[0].content).is_equal_to('chapter 1')

    assert_that(result[1].title).is_equal_to('title 2')
    assert_that(result[1].content).is_equal_to('chapter 2')

    assert_that(result[2].title).is_equal_to('title 3')
    assert_that(result[2].content).is_equal_to('chapter 3')

    assert_that(result[3].title).is_equal_to('title 4')
    assert_that(result[3].content).is_equal_to('chapter 4')

    assert_that(get_calls).is_length(2)
    assert_that(get_calls[0].args[0]).is_equal_to('http://example.com?page=2')
    assert_that(get_calls[1].args[0]).is_equal_to('http://example.com')
