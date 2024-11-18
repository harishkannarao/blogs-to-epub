from datetime import datetime, timezone
from pathlib import Path

import requests
from bs4 import BeautifulSoup
from ebooklib import epub


def get_all_chapters_from_url(initial_url: str, load_individual_page: bool) -> list[epub.EpubHtml]:
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
                href = ''
                for entry_link in entry['link']:
                    if entry_link['rel'] == 'alternate':
                        title = entry_link['title']
                        href = entry_link['href']
                if load_individual_page:
                    response = requests.get(href)
                    soup = BeautifulSoup(response.text, "html.parser")
                    html_content = soup.get_text(strip=True)
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


def convert_to_single_epub(output_dir: str, file_name: str, url: str, load_individual_page: bool):
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    chapters: list[epub.EpubHtml] = get_all_chapters_from_url(url, load_individual_page)
    write_to_epub(output_dir, file_name, url, chapters)
    return
