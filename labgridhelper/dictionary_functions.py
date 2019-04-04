def split_output_to_dict(command_protocoll, command, delimiter="=", strip_chars=""):
    '''
    returns a dictionary that contains the results of the command, where the key
    is the part before and the value is the part after the first delimiter optional
    chars can be specified to be stript from the value
    Args:
        command_protocoll: command_protocoll to execute command (shell, barebox, ...)
        command: command to execute
        delimiter: character that seperates key and value
        strip_chars: characters to strip from key and value
    Returns:
        output_dict: dictionary that contains the pairs of key and value
    '''
    command_output = command_protocoll.run_check(command)
    output_dict = {}
    for line in command_output:
        try:
            if line.count(delimiter) >= 1: # lines without a delimiter are ignored
                (key, value) = line.split(delimiter, 1)
                output_dict[key.strip(strip_chars)] = value.strip(strip_chars)
        except ValueError:
            pass
    return output_dict
