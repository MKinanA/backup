from argparse import ArgumentParser, _SubParsersAction, Namespace
from pathlib import Path
from .utils.database import database_read, get_or_set

def register_subparser(subparsers: _SubParsersAction[ArgumentParser]):
    parser = subparsers.add_parser('validate', help='Validate a backup schema, such as checking the provided paths.')
    parser.add_argument('name', type=str, help='Name of the backup schema.')
    parser.set_defaults(func=execute)

def execute(args: Namespace):
    schema_name = args.name
    schemas = get_or_set(database_read(), 'schemas', [])
    if not schema_name in (schema['name'] for schema in schemas): raise KeyError(f'(expected) Schema "{schema_name}" doesn\'t exist.')
    schema: dict = schemas[next((index for index in range(len(schemas)) if schemas[index]['name'] == schema_name))]
    if not Path(source_path := schema['source_path']).exists(): raise FileNotFoundError(f'(expected) Source path `{source_path}` doesn\'t exist.')
    if not ((backup_Path := Path(backup_path := schema['backup_path'])).exists() and backup_Path.is_dir()): raise FileNotFoundError(f'(expected) Backup path `{backup_path}` doesn\'t exist or isn\'t a directory.')
    print(f'Nothing wrong was detected in {schema_name}.')