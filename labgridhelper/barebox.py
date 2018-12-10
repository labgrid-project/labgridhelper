from labgrid.driver import BareboxDriver


def get_commands(command):
    """Returns the available commands of a running Barebox bootloader
    Args:
        command (BareboxDriver): An instance of the BareboxDriver
    Returns:
        list: list of the available commands
    """
    assert isinstance(command, BareboxDriver)
    out = command.run_check("help")
    commands = []
    for line in out:
        if line and line[0] == " ":
            for cmd in line.split(','):
                commands.append(cmd.strip(',').strip(" "))
    return commands

def get_globals(command):
    """Returns the global variables of a running Barebox bootloader
    Args:
        command (BareboxDriver): An instance of the BareboxDriver
    Returns:
        dict: name as key and value as key-value
    """
    assert isinstance(command, BareboxDriver)
    out = command.run_check("global")
    out = map(lambda x: x[2:], out)
    global_variables = {}
    for line in out:
        sep = line.index(":")
        key = line[:sep]
        value = line[sep+2:]
        global_variables[key] = value
    return global_variables
