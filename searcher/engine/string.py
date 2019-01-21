import re

def str_contains_numbers(str):
    return bool(re.search(r'\d', str))


def str_is_num_version(str):
    return bool(re.search(r'\d+((\.\d+)+)?', str))


def str_contains_num_version_range(str):
    return bool(re.search(r'\d+((\.\d+)+)? < \d+((\.\d+)+)?', str))


def str_contains_num_version_range_with_x(str):
    return bool(re.search(r'\d+((\.\d+)+)?(\.x)? < \d+((\.\d+)+)?(\.x)?', str))