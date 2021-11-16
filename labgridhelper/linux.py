import json
import re

from labgrid.protocol import CommandProtocol
from labgrid.driver import ExecutionError

def get_systemd_version(command):
    """Returns systemd version retrieved by parsing output of `systemd --version`

    Args:
        command (CommandProtocol): An instance of a Driver implementing the CommandProtocol

    Returns:
        int: systemd version number
    """
    assert isinstance(command, CommandProtocol), "command must be a CommandProtocol"

    out = command.run_check("systemctl --version")
    out = out[0]

    parsed = re.search(r'^systemd\s+(?P<version>\d+)', out)
    if not parsed:
        raise ValueError("Systemd version output changed")
    return int(parsed.group("version"))

def get_systemd_status(command):
    """Returns parsed output of systemd Manager's ListUnits DBus command

    Args:
        command (CommandProtocol): An instance of a Driver implementing the CommandProtocol

    Returns:
        dict: dictionary of service names to their properties
    """
    assert isinstance(command, CommandProtocol), "command must be a CommandProtocol"
    array_notation = "a(ssssssouso)"

    def get_systemd_status_json(command):
        out = command.run_check(
            "busctl call --json=short --no-pager org.freedesktop.systemd1 \
            /org/freedesktop/systemd1 org.freedesktop.systemd1.Manager ListUnits"
        )
        out = out[0]
        out = json.loads(out)
        if out["type"] != array_notation:
            raise ValueError("Systemd ListUnits output changed")

        services = {}
        for record in out["data"][0]:
            data = iter(record)
            name = next(data)
            services[name] = {}
            services[name]["description"] = next(data)
            services[name]["load"] = next(data)
            services[name]["active"] = next(data)
            services[name]["sub"] = next(data)
            services[name]["follow"] = next(data)
            services[name]["path"] = next(data)
            services[name]["id"] = int(next(data))
            services[name]["type"] = next(data)
            services[name]["objpath"] = next(data)

        return services

    def get_systemd_status_raw(command):
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
            path_and_id = next(data).split('\"')
            services[name]["path"] = path_and_id[0]
            services[name]["id"] = int(path_and_id[1].strip(" "))
            services[name]["type"] = path_and_id[2]
            services[name]["objpath"] = next(data)

        return services

    if get_systemd_version(command) > 239:
        return get_systemd_status_json(command)
    else:
        return get_systemd_status_raw(command)


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
    out.extend(command.run_check("ls /bin"))
    out.extend(command.run_check("ls /usr/sbin"))
    out.extend(command.run_check("ls /sbin"))
    if directories:
        assert isinstance(directories, list), "directories must be a list"
        for directory in directories:
            out.extend(command.run_check("ls {}".format(directory)))
    commands = set()
    for line in out:
        for cmd in line.split(" "):
            if cmd:
                commands.add(cmd)

    return commands

def get_systemd_service_active(command, service):
    """Returns True if service is active, False in all other cases

    Args:
        command (CommandProtocol): An instance of a Driver implementing the CommandProtocol
        service (str): name of the service

    Returns:
        bool: True if service is active, False otherwise
    """
    assert isinstance(command, CommandProtocol), "command must be a CommandProtocol"
    _, _, exitcode = command.run(
        "systemctl --quiet is-active {}".format(service)
    )
    return exitcode == 0

def get_interface_ip(command, interface="eth0"):
    """Returns the global valid IPv4 address of the supplied interface

    Args:
        command (CommandProtocol): An instance of a Driver implementing the CommandProtocol
        interface (string): name of the interface

    Returns:
        str: IPv4 address of the interface, None otherwise
    """
    assert isinstance(command, CommandProtocol), "command must be a CommandProtocol"

    try:
        ip_string = command.run_check("ip -o -4 addr show")
    except ExecutionError:
        return None

    regex = re.compile(
        r"""\d+:       # Match the leading number
        \s+(?P<if>\w+) # Match whitespace and interfacename
        \s+inet\s+(?P<ip>[\d.]+) # Match IP Adress
        /(?P<prefix>\d+) # Match prefix
        .*global # Match global scope, not host scope""", re.X
    )
    result = {}

    for line in ip_string:
        match = regex.match(line)
        if match:
            match = match.groupdict()
            result[match['if']] = match['ip']
    if result:
        return result[interface]

    return None

def get_hostname(command):
    """Returns the hostname

    Args:
        command (CommandProtocol): An instance of a Driver implementing the CommandProtocol

    Returns:
        str: hostname of the target, None otherwise
    """
    assert isinstance(command, CommandProtocol), "command must be a CommandProtocol"

    try:
        hostname_string = command.run_check("hostname")
    except ExecutionError:
        return None
    return hostname_string[0]

def systemd_unit_properties(command, unit_properties, unit=''):
    """Yields the values of the properties of a unit

    Args:
        command (CommandProtocol): An instance of a Driver implementing the CommandProtocol
        unit_properties (iterable): Names of the properties of interest
        unit (str, optional): The systemd unit of interest, defaults to empty (systemd manager itself)

    Yields:
        str: Property value of the unit
    """
    assert isinstance(command, CommandProtocol), "command must be a CommandProtocol"

    for unit_property in unit_properties:
        yield command.run_check('systemctl --property={property} --no-pager --value show {unit}'.format(
            property=unit_property, unit=unit))[0]
