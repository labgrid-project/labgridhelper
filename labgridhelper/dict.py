def split_to_dict(command_output, delimiter="=", strip_chars=""):
    '''
    returns a dictionary that splits the content of the command_output.
    The key is the part before and the value is the part after the first
    delimiter. Optional chars can be specified to be stript from key and
    value.
    Args:
        command_output: output to split into dict
        delimiter: character that seperates key and value
        strip_chars: characters to strip from key and value
    Returns:
        output_dict: dictionary that contains the pairs of key and value
    '''
    output_dict = {}
    for line in command_output:
        try:
            if delimiter in line: # lines without a delimiter are ignored
                (key, value) = line.split(delimiter, 1)
                output_dict[key.strip(strip_chars)] = value.strip(strip_chars)
        except ValueError:
            pass
    return output_dict
