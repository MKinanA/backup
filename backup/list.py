from argparse import ArgumentParser, _SubParsersAction, Namespace
from .utils.database import database_read

def register_subparser(subparsers: _SubParsersAction[ArgumentParser]):
    parser = subparsers.add_parser('list', help='List created backup schemas.')
    parser.set_defaults(func=execute)

def execute(args: Namespace):
    schemas: list = database_read().get('schemas', [])
    for schema in schemas: print(schema['name'])