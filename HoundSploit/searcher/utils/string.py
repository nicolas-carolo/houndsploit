import re


def str_contains_num_version(str):
    return bool(re.search(r' \d+((\.\d+)+)?', str))


def str_is_num_version(str):
    return bool(re.search(r'\d+((\.\d+)+)?', str))


def str_contains_software_name_and_num_version(text):
    if str_contains_num_version(str(text)) and str(text).__contains__(' ') and not str(text).__contains__('<'):
        return True
    else:
        return False