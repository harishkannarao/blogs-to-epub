import requests
from bs4 import BeautifulSoup
from ebooklib import epub
from pathlib import Path
from dateutil.parser import parse


def create_epub(file, blog_id, title, html_content, author, href, published, updated):
    html_chapter = epub.EpubHtml(title=title, file_name="html.xhtml", lang='en')
    html_chapter.content = html_content

    meta_content = f"""
    <h1>Meta Data</h1>
    <p>Author: {author}</p>
    <p>Url: {href}</p>
    <p>Published: {published}</p>
    <p>Updated: {updated}</p>
    """
    meta_chapter = epub.EpubHtml(title='Meta Data', file_name="meta.xhtml", lang='en')
    meta_chapter.content = meta_content

    chapters = [html_chapter, meta_chapter]

    book = epub.EpubBook()

    # add metadata
    book.set_identifier(blog_id)
    book.set_title(title)
    book.set_language('en')
    book.add_author(author)

    # add chapters to the book
    for chapter in chapters:
        book.add_item(chapter)

    # create table of contents
    book.toc = chapters

    # add navigation files
    book.add_item(epub.EpubNcx())
    book.add_item(epub.EpubNav())

    # create spine
    book.spine = chapters

    # create epub file
    epub.write_epub(file, book, {})


def convert_blog(output_dir, entry, load_individual_page):
    blog_id = entry['id']['$t']
    author = entry['author'][0]['name']['$t']
    alternate_link = next((link for link in entry['link'] if link['rel'] == 'alternate'), None)
    title = alternate_link['title']
    file_name = title.replace('*', '')
    html_content = entry['content']['$t']
    href = alternate_link['href']
    if load_individual_page:
        response = requests.get(href)
        soup = BeautifulSoup(response.text, "html.parser")
        html_content = soup.get_text(strip=True)
    published_str = entry['published']['$t']
    updated_str = entry['updated']['$t']
    published_timestamp = parse(published_str)
    published_year = published_timestamp.year
    published_month = published_timestamp.month
    published_day = published_timestamp.day
    full_dir = f"{output_dir}/{published_year}/{published_month}/{published_day}"
    Path(full_dir).mkdir(parents=True, exist_ok=True)
    create_epub(f"{full_dir}/{file_name}.epub", blog_id, title, html_content, author, href, published_str, updated_str)


def download_blog_posts(output_dir, input_url, load_individual_page: bool):
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    response = requests.get(input_url)
    res_json = response.json()
    if 'entry' in res_json['feed']:
        for entry in res_json['feed']['entry']:
            convert_blog(output_dir, entry, load_individual_page)

    return next((link['href'] for link in res_json['feed']['link'] if link['rel'] == 'next'), None)


def download_all(output_dir, input_url, load_individual_page: bool):
    url = input_url

    while url is not None:
        url = download_blog_posts(output_dir, url, load_individual_page)
