import argparse

from utils import convert_to_epub as convert_epub

my_parser = argparse.ArgumentParser(description='Convert blog post(s) as single epub')

my_parser.add_argument('--dir', '-d', action='store', type=str, required=True)
my_parser.add_argument('--name', '-n', action='store', type=str, required=True)
my_parser.add_argument('--url', '-u', action='store', type=str, required=True)

args = my_parser.parse_args()

convert_epub(args.dir, args.name, args.url)