from argparse import ArgumentParser
from pathlib import Path
from . import list, create

DATABASE_PATH = (Path(__file__).parent / 'database.json').resolve()

def main():
    if not DATABASE_PATH.exists():
        with open(DATABASE_PATH, 'w') as database_file: database_file.write('{}')

    parser = ArgumentParser(description='Simple backup utility')
    subparsers = parser.add_subparsers(required=True)

    list.register_subparser(subparsers)
    create.register_subparser(subparsers)

    args = parser.parse_args()

    args.func(args)

if __name__ == '__main__': main()