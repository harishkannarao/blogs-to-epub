from assertpy import assert_that
from ebooklib import epub

from blog_to_epub.util.utils import write_to_epub
from blog_to_epub.util.utils import get_all_chapters_from_url
from blog_to_epub.util.utils import convert_to_single_epub
from tests.unit.conftest import WriteEpubCall, ArgsKwArgsPair, MockGetResponse, MkdirCall
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


def test__get_all_chapters_from_url__returns_all_chapters_from_url(
        requests_get_fixture: (list[ArgsKwArgsPair], list[MockGetResponse])
):
    get_calls: list[ArgsKwArgsPair] = requests_get_fixture[0]
    get_mock_responses: list[MockGetResponse] = requests_get_fixture[1]

    get_mock_responses.extend([
        create_blog_response(
            next_link='http://example.com?page=2',
            chapters=[
                ('title 4', 'chapter 4'),
                ('title 3', 'chapter 3'),
            ]),
        create_blog_response(
            next_link=None,
            chapters=[
                ('title 2', 'chapter 2'),
                ('title 1', 'chapter 1'),
            ]),
    ])

    result = get_all_chapters_from_url('http://example.com', False)

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
    assert_that(get_calls[0].args[0]).is_equal_to('http://example.com')
    assert_that(get_calls[1].args[0]).is_equal_to('http://example.com?page=2')


def test__convert_to_single_epub__converts_given_url_to_epub(
        path_mkdir_fixture: list[MkdirCall],
        requests_get_fixture: (list[ArgsKwArgsPair], list[MockGetResponse]),
        epub_write_fixture: list[WriteEpubCall]
):
    get_calls: list[ArgsKwArgsPair] = requests_get_fixture[0]
    get_mock_responses: list[MockGetResponse] = requests_get_fixture[1]
    get_mock_responses.extend([
        create_blog_response(
            next_link='http://www.example.com?page=2',
            chapters=[
                ('title 4', 'chapter 4'),
                ('title 3', 'chapter 3'),
            ]
        ),
        create_blog_response(
            next_link=None,
            chapters=[
                ('title 2', 'chapter 2'),
                ('title 1', 'chapter 1'),
            ]
        ),
        create_blog_response(
            next_link=None,
            chapters=[
                ('title 2', 'chapter 2'),
                ('title 1', 'chapter 1'),
            ]
        ),
        create_blog_response(
            next_link='http://www.example.com?page=2',
            chapters=[
                ('title 4', 'chapter 4'),
                ('title 3', 'chapter 3'),
            ]
        ),
    ])

    convert_to_single_epub(
        "/tmp/dir",
        "out_file",
        "http://www.example.com",
        False
    )

    assert_that(path_mkdir_fixture).is_length(1)
    assert_that(path_mkdir_fixture[0].path).is_equal_to('/tmp/dir')
    assert_that(path_mkdir_fixture[0].argsPair.args).is_length(0)
    assert_that(path_mkdir_fixture[0].argsPair.kwargs.get('parents')).is_true()
    assert_that(path_mkdir_fixture[0].argsPair.kwargs.get('exist_ok')).is_true()

    assert_that(epub_write_fixture).is_length(1)
    assert_that(epub_write_fixture[0].name).is_equal_to('/tmp/dir/out_file.epub')
    assert_that(epub_write_fixture[0].options).is_equal_to({})

    result = epub_write_fixture[0].book
    assert_that(result.items).is_length(7)

    meta_chapter: epub.EpubHtml = result.items[0]
    assert_that(meta_chapter.content).contains("Url: " + "http://www.example.com")

    assert_that(result.items[1].content).is_same_as('chapter 1')
    assert_that(result.items[2].content).is_same_as('chapter 2')
    assert_that(result.items[3].content).is_same_as('chapter 3')
    assert_that(result.items[4].content).is_same_as('chapter 4')

    assert_that(result.items[5]).is_instance_of(epub.EpubNcx)
    assert_that(result.items[6]).is_instance_of(epub.EpubNav)

    assert_that(get_calls).is_length(2)
    assert_that(get_calls[0].args[0]).is_equal_to('http://www.example.com')
    assert_that(get_calls[1].args[0]).is_equal_to('http://www.example.com?page=2')
