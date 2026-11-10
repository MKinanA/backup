from argparse import ArgumentParser, _SubParsersAction, Namespace
from .utils.database import database_read, get_or_set

def register_subparser(subparsers: _SubParsersAction[ArgumentParser]):
    parser = subparsers.add_parser('info', help='Check the information (fields) of a backup schema.')
    parser.add_argument('name', type=str, help='Name of the backup schema.')
    parser.set_defaults(func=execute)

def execute(args: Namespace):
    schema_name = args.name
    schemas = get_or_set(database_read(), 'schemas', [])
    if not schema_name in (schema['name'] for schema in schemas): raise KeyError(f'(expected) Schema "{schema_name}" doesn\'t exist.')
    schema: dict = schemas[next((index for index in range(len(schemas)) if schemas[index]['name'] == schema_name))]
    longest_field_name = max(len(field_name) for field_name in schema.keys())
    for field, value in schema.items(): print(f'{field}{' ' * (longest_field_name - len(str(field)))}: {'"' if type(value) == str else ''}{value}{'"' if type(value) == str else ''}')