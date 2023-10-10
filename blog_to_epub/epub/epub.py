from blog_to_epub.util.utils import convert_to_single_epub as convert_single_epub
from blog_to_epub.multiple.multiple import download_all
import argparse

my_parser = argparse.ArgumentParser(description='Convert blog post(s) as single epub')

my_parser.add_argument('--dir', '-d', action='store', type=str, required=True)
my_parser.add_argument('--url', '-u', action='store', type=str, required=True)
my_parser.add_argument('--single-file', '-sf', action='store_true', required=False)
my_parser.add_argument('--name', '-n', action='store', type=str, required=False)

args = my_parser.parse_args()


def download_epub():
    if args.single_file:
        if args.name is None:
            raise SystemExit('error: argument --name/-n is expected when --single-file/-sf is set')
        convert_single_epub(args.dir, args.name, args.url)
    else:
        download_all(args.dir, args.url)
    return
