from subprocess import run, CalledProcessError
from argparse import ArgumentParser
from .utils.check_command_availability import check_command_availability

parser = ArgumentParser(description='Simple backup utility')
parser.add_argument_group('')

if not check_command_availability('tar'):
    print('Error, `tar` is unavailable.')
    raise SystemExit

command = ['sudo', 'whoami']

print(f'Executing `{' '.join(command)}`')
try: process = run(command, check=True)
except FileNotFoundError: raise
except CalledProcessError: raise

print('Finished')