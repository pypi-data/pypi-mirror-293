from argparse import ArgumentParser
from feather_converter import converter

def main():
    parser = ArgumentParser(description="File Operations CLI")

    parser.add_argument("convert", help="Convert feather to csv.")
    parser.add_argument('--file', type=str, help="Feather file to convert")
    parser.add_argument('--out', type=str, help="Feather file to convert")


    args = parser.parse_args()
    
    if args.convert == "convert":
        converter.convert_feather(args.file, args.out)
    else:
        parser.print_help()