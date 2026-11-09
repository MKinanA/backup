from shutil import which

def check_command_availability(command) -> bool: return which('tar') is not None