from sys import platform
if platform != 'linux': raise SystemExit('This tool is intended for Linux only.')

from argparse import ArgumentParser
from pathlib import Path
from . import list, create, delete, schedule

DATABASE_PATH = (Path(__file__).parent / 'database.json').resolve()

def main():
    if not DATABASE_PATH.exists():
        with open(DATABASE_PATH, 'w') as database_file: database_file.write('{}')

    parser = ArgumentParser(description='Simple backup tool for Linux.')
    subparsers = parser.add_subparsers(required=True)

    list.register_subparser(subparsers)
    create.register_subparser(subparsers)
    delete.register_subparser(subparsers)
    schedule.register_subparser(subparsers)

    args = parser.parse_args()

    try: args.func(args)
    except BaseException as e:
        if str(e).lower().startswith(expected_error_flag := '(expected) '): raise SystemExit(f'Error: {str(e)[len(expected_error_flag):]}')
        else:
            print('An unexpected exception occurred.')
            raise e

if __name__ == '__main__': main()