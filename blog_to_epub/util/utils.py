import requests
from pathlib import Path
from ebooklib import epub
from datetime import datetime, timezone


def get_all_chapters_from_url(initial_url: str) -> list[epub.EpubHtml]:
    chapters: list[epub.EpubHtml] = []
    chapter_index = 1
    url = initial_url
    while url is not None:
        response = requests.get(url)
        res_json = response.json()
        url = None
        for link in res_json['feed']['link']:
            if link['rel'] == 'next':
                url = link['href']
        if 'entry' in res_json['feed']:
            for entry in res_json['feed']['entry']:
                html_content = entry['content']['$t']
                title = ''
                for entry_link in entry['link']:
                    if entry_link['rel'] == 'alternate':
                        title = entry_link['title']
                html_chapter = epub.EpubHtml(title=title, file_name=f"chapter_{chapter_index}.xhtml", lang='en')
                html_chapter.content = html_content
                chapter_index = chapter_index + 1
                chapters.append(html_chapter)
    chapters.reverse()
    return [*chapters]


def write_to_epub(output_dir: str, file_name: str, url: str, chapters: list[epub.EpubHtml]) -> None:
    meta_content = f"""
        <h1>Meta Data</h1>
        <p>Url: {url}</p>
        <p>Generated: {datetime.now(timezone.utc).isoformat()}</p>
        """
    meta_chapter = epub.EpubHtml(title='Meta Data', file_name="meta.xhtml", lang='en')
    meta_chapter.content = meta_content

    all_chapters = [meta_chapter]
    all_chapters.extend(chapters)

    book = epub.EpubBook()
    book.set_identifier(url)
    book.set_title(file_name)
    book.set_language('en')
    book.add_author('Unknown')

    for chapter in all_chapters:
        book.add_item(chapter)

    book.toc = all_chapters

    # add navigation files
    book.add_item(epub.EpubNcx())
    book.add_item(epub.EpubNav())

    # create spine
    book.spine = all_chapters

    # create epub file
    epub.write_epub(f"{output_dir}/{file_name}.epub", book, {})


def convert_to_single_epub(output_dir: str, file_name: str, url: str):
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    chapters: list[epub.EpubHtml] = get_all_chapters_from_url(url)
    write_to_epub(output_dir, file_name, url, chapters)
    return
