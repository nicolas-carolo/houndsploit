import re


def str_contains_numbers(str):
    """
    Check if a string contains at least one number.
    :param str: the string to check.
    :return: true if the string contains at least one number, false else.
    """
    return bool(re.search(r'\d', str))


def str_is_num_version(str):
    """
    Check if a string contains a number of version.
    :param str: the string to check.
    :return: true if the string contains a number of version, false else.
    """
    return bool(re.search(r' \d+((\.\d+)+)?', str))

def word_is_num_version(str):
    """
    Check if a word contains a number of version.
    :param str: the word to check.
    :return: true if the word contains a number of version, false else.
    """
    return bool(re.search(r'\d+((\.\d+)+)?', str))


def str_contains_num_version_range(str):
    """
    Check if a string contains a range of number version.
    :param str: the string to check.
    :return: true if the string contains a a range of number version, false else.
    """
    return bool(re.search(r'\d+((\.\d+)+)? < \d+((\.\d+)+)?', str))


def str_contains_num_version_range_with_x(str):
    """
    Check if a string contains a range of number version with x.
    :param str: the string to check.
    :return: true if the string contains a a range of number version with x, false else.
    """
    return bool(re.search(r'\d+((\.\d+)+)?(\.x)? < \d+((\.\d+)+)?(\.x)?', str))
