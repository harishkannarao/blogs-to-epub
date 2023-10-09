import argparse
import requests
from pathlib import Path

my_parser = argparse.ArgumentParser(description='Convert blog post(s) as single epub')

my_parser.add_argument('--dir', '-d', action='store', type=str, required=True)
my_parser.add_argument('--name', '-n', action='store', type=str, required=True)
my_parser.add_argument('--url', '-u', action='store', type=str, required=True)

args = my_parser.parse_args()

def get_all_urls(initial_url):
    all_urls = []
    url = initial_url
    while url is not None:
        print(url)
        all_urls.append(url)
        response = requests.get(url)
        res_json = response.json()
        url = next((link['href'] for link in res_json['feed']['link'] if link['rel'] == 'next'), None)

    return all_urls

def convert_to_epub(output_dir, file_name, url):
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    urls = get_all_urls(url)
    print(urls)
    return

convert_to_epub(args.dir, args.name, args.url)