from argparse import ArgumentParser, _SubParsersAction, Namespace
from .utils.database import database_write, get_or_set

def register_subparser(subparsers: _SubParsersAction[ArgumentParser]):
    parser = subparsers.add_parser('delete', help='Delete a backup schema.')
    parser.add_argument('name', type=str, help='Name of the backup schema.')
    parser.set_defaults(func=execute)

def execute(args: Namespace):
    schema_name = args.name
    with database_write() as db:
        if 'schemas' not in db: return
        schemas: list = db['schemas']
        schema_index = next((index for index in range(len(schemas)) if schemas[index]['name'] == schema_name), None)
        if schema_index is not None: del schemas[schema_index]