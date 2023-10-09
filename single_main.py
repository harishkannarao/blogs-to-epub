import argparse
from pathlib import Path

my_parser = argparse.ArgumentParser(description='Convert blog post(s) as single epub')

my_parser.add_argument('--dir', '-d', action='store', type=str, required=True)
my_parser.add_argument('--name', '-n', action='store', type=str, required=True)
my_parser.add_argument('--url', '-u', action='store', type=str, required=True)

args = my_parser.parse_args()

def convert_to_epub(output_dir, file_name, url):
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    return

convert_to_epub(args.dir, args.name, args.url)