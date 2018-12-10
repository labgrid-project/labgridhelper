from labgrid.protocol import CommandProtocol

def get_systemd_status(command):
    assert isinstance(command, CommandProtocol), "command must be a CommandProtocol"
    # TODO: Use busctl --json if systemd>239
    array_notation = "a(ssssssouso)"
    out = command.run_check(
        "busctl call --no-pager org.freedesktop.systemd1 \
        /org/freedesktop/systemd1 org.freedesktop.systemd1.Manager ListUnits"
    )

    out = out[0]
    if array_notation not in out:
        raise ValueError("Systemd ListUnits output changed")
    out = out[len(array_notation):]
    array_length = int(out[:out.index('"')].strip(" "))
    out = out[out.index('"')+1:-1]
    out = out.split('\" \"')
    data = iter(out)
    services = {}
    for _ in range(array_length):
        name = next(data)
        services[name] = {}
        services[name]["description"] = next(data)
        services[name]["load"] = next(data)
        services[name]["active"] = next(data)
        services[name]["sub"] = next(data)
        services[name]["follow"] = next(data)
        path_and_id = next(data)
        pos = path_and_id.index('"')
        services[name]["path"] = path_and_id[:pos]
        services[name]["id"] = int(path_and_id[pos+1:-1].strip(" "))
        services[name]["type"] = path_and_id[path_and_id.rfind('"'):]
        services[name]["objpath"] = next(data)

    return services

def get_commands(command, directories=None):
    """Returns the commands of a running linux system
    Args:
        command (CommandProtocol): An instance of a Driver implementing the CommandProtocol
        directories (list): An optional list of directories to include
    Returns:
        list: list of commands available under linux
    """
    assert isinstance(command, CommandProtocol), "command must be a CommandProtocol"
    out = command.run_check("ls /usr/bin")
    out.extend(command.run_check("ls /usr/sbin"))
    if directories:
        assert isinstance(directories, list), "directories must be a list"
        for directory in directories:
            out.extend(command.run_check("ls {}".format(directory)))
    commands = []
    for line in out:
        for cmd in line.split(" "):
            if cmd:
                commands.append(cmd)

    return commands
