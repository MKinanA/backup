from argparse import ArgumentParser, _SubParsersAction, Namespace
from .utils.database import database_write, get_or_set

def register_subparser(subparsers: _SubParsersAction[ArgumentParser]):
    parser = subparsers.add_parser('delete', help='Delete a backup schema.')
    parser.add_argument('name', type=str)
    parser.set_defaults(func=execute)

def execute(args: Namespace):
    with database_write() as db:
        if 'schemas' not in db: return
        schema_name = args.name
        schemas: list = db['schemas']
        schema_index = next((index for index in range(len(schemas)) if schemas[index]['name'] == schema_name), None)
        if schema_index is not None: del schemas[schema_index]