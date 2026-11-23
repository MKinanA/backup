from argparse import ArgumentParser, _SubParsersAction, Namespace
from crontab import CronItem
from .utils.database import database_read, database_write, get_or_set
from .utils.expected_exception import expected_exception as expected
from .schedule import get_crontab, profile_cron

def register_subparser(subparsers: _SubParsersAction[ArgumentParser]):
    parser = subparsers.add_parser('delete', help='Delete a backup profile.')
    parser.add_argument('name', type=str, help='Name of the backup profile.')
    parser.set_defaults(func=execute)

def execute(args: Namespace, skip_cron_check: bool = False):
    profile_name = args.name
    profiles = get_or_set(database_read(), 'profiles', [])
    if not profile_name in (profile['name'] for profile in profiles): raise expected(KeyError(f'Profile "{profile_name}" doesn\'t exist.'))
    if not skip_cron_check:
        try:
            if isinstance(profile_cron(profile_name, get_crontab()), CronItem):
                e = expected(ValueError(f'Profile "{profile_name}" is scheduled to run automatically. Unschedule it first before deleting it.'))
                setattr(e, 'cron_exists', True)
                raise e
        except Exception as e:
            if getattr(e, 'cron_exists', False): raise e
            while True:
                if (confirm := input('Failed to check if the profile is scheduled and has a cron job, delete anyway? [y/n]: ').lower()) in ('y', 'ye', 'yes'): break
                elif confirm in ('n', 'no'): return 1
    with database_write() as db:
        profiles = get_or_set(db, 'profiles', [])
        del profiles[next((index for index in range(len(profiles)) if profiles[index]['name'] == profile_name))]
    print(f'Deleted backup profile "{profile_name}".')