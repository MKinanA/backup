from argparse import ArgumentParser, _SubParsersAction, Namespace
from pathlib import Path
from crontab import CronTab, CronSlices
from .utils.database import database_read, get_or_set

UNSCHEDULING_KEYWORDS = ('unschedule', 'delete', 'remove', 'none', 'null', 'never', 'inactive', 'deactivate', 'disable')

def register_subparser(subparsers: _SubParsersAction[ArgumentParser]):
    parser = subparsers.add_parser('create', help='Create a new backup schema.')
    parser.add_argument('name', type=str, help='Name of the backup schema.')
    parser.add_argument('-s', '--set', metavar='<cron_expression>', type=validate_schedule_expression, help=f'Either a cron expression for the scheduling, or {'/'.join(UNSCHEDULING_KEYWORDS)} to unschedule the schema.')
    parser.set_defaults(func=execute)

def execute(args: Namespace):
    return # TODO: Unfinished
    schema_name = args.name
    schemas = get_or_set(database_read(), 'schemas', [])
    if not schema_name in (schema['name'] for schema in schemas): raise KeyError(f'(expected) Schema "{schema_name}" doesn\'t exist.')

def validate_schedule_expression(expression: str) -> str | None:
    if CronSlices.is_valid(expression): return expression
    elif expression.lower() in UNSCHEDULING_KEYWORDS: return None
    else: raise ValueError('(expected) Invalid cron schedule expression.')