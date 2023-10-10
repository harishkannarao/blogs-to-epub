import requests
from pathlib import Path
from ebooklib import epub
from datetime import datetime, timezone


def get_all_urls(initial_url):
    all_urls = []
    url = initial_url
    while url is not None:
        all_urls.append(url)
        response = requests.get(url)
        res_json = response.json()
        url = None
        for link in res_json['feed']['link']:
            if link['rel'] == 'next':
                url = link['href']

    return all_urls


def get_all_chapters(urls):
    chapters = []
    chapter_index = 1
    for url in reversed(urls):
        response = requests.get(url)
        res_json = response.json()
        if 'entry' in res_json['feed']:
            for entry in reversed(res_json['feed']['entry']):
                html_content = entry['content']['$t']
                title = ''
                for entry_link in entry['link']:
                    if entry_link['rel'] == 'alternate':
                        title = entry_link['title']
                html_chapter = epub.EpubHtml(title=title, file_name=f"chapter_{chapter_index}.xhtml", lang='en')
                html_chapter.content = html_content
                chapter_index = chapter_index + 1
                chapters.append(html_chapter)
    return chapters


def write_to_epub(output_dir, file_name, url, chapters):
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


def convert_to_single_epub(output_dir, file_name, url):
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    urls = get_all_urls(url)
    chapters = get_all_chapters(urls)
    write_to_epub(output_dir, file_name, url, chapters)
    return
