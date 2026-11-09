from argparse import ArgumentParser, _SubParsersAction, Namespace
from .utils.database import database_write, get_or_set

def register_subparser(subparsers: _SubParsersAction[ArgumentParser]):
    parser = subparsers.add_parser('create', help='Create a new backup schema.')
    parser.add_argument('name', type=str)
    parser.set_defaults(func=execute)

def execute(args: Namespace):
    with database_write() as db:
        schema_name = args.name
        schemas: list = get_or_set(db, 'schemas', [])
        if schema_name not in (schema['name'] for schema in schemas): schemas.append({'name': schema_name})