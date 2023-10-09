import requests
from pathlib import Path

def get_all_urls(initial_url):
    all_urls = []
    url = initial_url
    while url is not None:
        print(url)
        all_urls.append(url)
        response = requests.get(url)
        res_json = response.json()
        url = None
        links = res_json['feed']['link']
        for link in links:
            if link['rel'] == 'next':
                url = link['href']

    return all_urls

def convert_to_epub(output_dir, file_name, url):
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    urls = get_all_urls(url)
    print(urls)
    return