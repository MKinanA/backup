from argparse import ArgumentParser, _SubParsersAction, Namespace
from pathlib import Path
from datetime import datetime
from tarfile import open as opentar
from .validate import validate_schema
from .utils.database import database_read, get_or_set

def register_subparser(subparsers: _SubParsersAction[ArgumentParser]):
    parser = subparsers.add_parser('run', help='Run a backup schema, creating an archive of the source file/directory and storing it in the backup directory.')
    parser.add_argument('name', type=str, help='Name of the backup schema.')
    parser.set_defaults(func=execute)

def execute(args: Namespace):
    schema_name = args.name
    schemas = get_or_set(database_read(), 'schemas', [])
    if not schema_name in (schema['name'] for schema in schemas): raise KeyError(f'(expected) Schema "{schema_name}" doesn\'t exist.')
    schema: dict = schemas[next((index for index in range(len(schemas)) if schemas[index]['name'] == schema_name))]
    validate_schema(schema)

    with opentar(backup_tar_path := ((backup_path := Path(schema['backup_path'])) / f'{datetime.now().strftime("%Y-%m-%d-%H-%M-%S")}.tar.gz'), 'w:gz') as backup_tar:
        if (source_path := Path(schema['source_path'])).is_dir():
            print('`source_path` is a directory, iterating...')
            for path in source_path.iterdir():
                print(f'> {path.name}')
                backup_tar.add(path, arcname=path.name)
        else:
            print('`source_path` is not a directory, copying into backup archive...')
            backup_tar.add(source_path, arcname=source_path.name)
    print(f'Done, backup archive stored in `{backup_path}` as `{backup_tar_path.name}`.')