from argparse import ArgumentParser, _SubParsersAction, Namespace
from .utils.database import database_write, get_or_set
from .utils.expected_exception import expected_exception as expected

def register_subparser(subparsers: _SubParsersAction[ArgumentParser]):
    parser = subparsers.add_parser('delete', help='Delete a backup schema.')
    parser.add_argument('name', type=str, help='Name of the backup schema.')
    parser.set_defaults(func=execute)

def execute(args: Namespace):
    schema_name = args.name
    with database_write() as db:
        if 'schemas' not in db: return
        schemas = get_or_set(db, 'schemas', [])
        if not schema_name in (schema['name'] for schema in schemas): raise expected(KeyError(f'Schema "{schema_name}" doesn\'t exist.'))
        del schemas[next((index for index in range(len(schemas)) if schemas[index]['name'] == schema_name))]
    print(f'Deleted backup schema "{schema_name}".')