from argparse import ArgumentParser, _SubParsersAction, Namespace
from pathlib import Path
from .utils.database import database_write, get_or_set

def register_subparser(subparsers: _SubParsersAction[ArgumentParser]):
    parser = subparsers.add_parser('create', help='Create a new backup schema.')
    parser.add_argument('name', type=str, help='Name of the backup schema.')
    parser.add_argument('source_path', type=Path, help='Location of the backup source (what you want to back up), can be either a file or a directory (folder).')
    parser.add_argument('backup_path', type=Path, help='Location of the backup destination (where you want the backups stored), must be a directory (duhh).')
    parser.set_defaults(func=execute)

def execute(args: Namespace):
    schema_name = args.name
    with database_write() as db:
        schemas: list = get_or_set(db, 'schemas', [])
        if schema_name in (schema['name'] for schema in schemas): raise ValueError(f'(expected) Backup schema named "{schema_name}" already exists.')
        else: schemas.append({
            'name': schema_name,
            'source_path': str(args.source_path.resolve()),
            'backup_path': str(args.backup_path.resolve()),
        })
    print(f'Created new backup schema "{schema_name}".')