from sys import platform, exit
if platform != 'linux': raise SystemExit('This tool is intended for Linux only.')

from argparse import ArgumentParser
from pathlib import Path
from . import list, create, info, modify, validate, run, check, schedule, delete
from .utils.expected_exception import EXPECTED_EXCEPTION_ATTR

DATABASE_PATH = (Path(__file__).parent / 'database.json').resolve()

def main() -> int:
    if not DATABASE_PATH.exists():
        with open(DATABASE_PATH, 'w') as database_file: database_file.write('{}')

    parser = ArgumentParser(description='Simple backup tool for Linux.')
    subparsers = parser.add_subparsers(required=True)

    list.register_subparser(subparsers)
    create.register_subparser(subparsers)
    info.register_subparser(subparsers)
    modify.register_subparser(subparsers)
    validate.register_subparser(subparsers)
    run.register_subparser(subparsers)
    check.register_subparser(subparsers)
    schedule.register_subparser(subparsers)
    delete.register_subparser(subparsers)

    args = parser.parse_args()

    try: return 0 if (exit_code := args.func(args)) is None else exit_code
    except BaseException as e:
        if getattr(e, EXPECTED_EXCEPTION_ATTR, False): raise SystemExit(f'Error: {' '.join(str(arg) for arg in e.args)}')
        else:
            print('An unexpected exception occurred.')
            raise e

if __name__ == '__main__': exit(main())