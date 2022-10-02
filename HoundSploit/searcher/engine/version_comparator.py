import re
from pkg_resources import parse_version


def is_lte_with_comparator_x(num_version, software_name, description):
    num_to_compare = get_num_version_with_comparator(software_name, description)
    if num_to_compare is not None:
        num_version = get_num_version_rounded(num_version, num_to_compare)
        return is_lte(num_version, num_to_compare)
    else:
        return False


def is_equal_with_x(num_version, num_to_compare):
    num_version = get_num_version_rounded(num_version, num_to_compare)
    if num_version is not None and num_to_compare is not None:
        return is_equal(num_version, num_to_compare)
    else:
        return False
    


def is_lte(num_version, num_to_compare):
    if parse_version(num_version) <= parse_version(num_to_compare):
        return True
    else:
        return False


def is_equal(num_version, num_to_compare):
    if parse_version(num_version) == parse_version(num_to_compare):
        return True
    else:
        return False


def get_num_version_without_comparator(software_name, description):
    regex_filter = r' \d+((\.\d+)+)?'
    num_version = get_num_version(software_name, description, regex_filter)
    return num_version


def get_num_version_with_comparator(software_name, description):
    regex_filter = r' < \d+((\.\d+)+)?'
    num_version = get_num_version(software_name, description, regex_filter)
    return num_version


def get_num_version(software_name, description, regex_filter):
    software_name = software_name.upper()
    description = description.upper()
    regex_filter = software_name + regex_filter
    software = extract_software_from_description(software_name, description, regex_filter)
    num_version = extract_num_version_from_software(software)
    return num_version
    

def extract_software_from_description(software_name, description, regex_filter):
    regex = re.search(regex_filter, description)
    try:
        software = regex.group(0)
        return software
    except AttributeError:
        return None


def extract_num_version_from_software(software):
    regex = re.search(r'\d+((\.\d+)+)?', software)
    try:
        num_version = regex.group(0)
        return num_version
    except AttributeError:
        return None


def get_num_version_rounded(num_version, num_to_compare):
    version_precision = str(num_to_compare).count('.')
    try:
        regex = re.search(r'\d+(\.\d+){0,%d}' % version_precision, num_version)
        num_version = regex.group()
        return num_version
    except AttributeError:
        return None


def is_in_version_range(num_version, software_name, description):
    """
    Check if the number of version (without x) of the software searched by the user is contained in the range of
    version in the vulnerability's description.
    :param num_version: the number of version searched by the user.
    :param software_name: the name of the software searched by the user.
    :param description: the vulnerability's description in which to do the check.
    :return: True if the number of version (without x) of the software searched by the user is contained in the range of
        version in the vulnerability's description, False else.
    """
    software_name = software_name.upper()
    description = description.upper()
    regex = re.search(software_name + r' \d+((\.\d+)+)? < \d+((\.\d+)+)?', description)
    try:
        software = regex.group(0)
        regex = re.search(r'(?P<from_version>\d+((\.\d+)+)?) < (?P<to_version>\d+((\.\d+)+)?)', software)
        if parse_version(num_version) >= parse_version(regex.group('from_version')) and parse_version(
                num_version) <= parse_version(regex.group('to_version')):
            return True
        else:
            return False
    except AttributeError:
        return False


def is_in_version_range_with_x(num_version, software_name, description):
    """
    Check if the number of version (with x) of the software searched by the user is contained in the range of
    version in the vulnerability's description.
    :param num_version: the number of version searched by the user.
    :param software_name: the name of the software searched by the user.
    :param description: the vulnerability's description in which to do the check.
    :return: True if the number of version (without x) of the software searched by the user is contained in the range of
                version in the vulnerability's description, False else.
    """
    software_name = software_name.upper()
    description = description.upper()
    regex = re.search(software_name + r' \w+((\.\w+)+)?(\.x)? < \w+((\.\w+)+)?(\.x)?', description)
    try:
        software = regex.group(0)
        regex = re.search(
            r'(?P<from_version>\d+((\.\d+)+)?)(\.X)? < (?P<to_version>\d+((\.\d+)+)?(\.X)?)',
            software)
        from_version = regex.group('from_version')
        to_version = regex.group('to_version')
        regex = re.search(r'(?P<base>.+)\.(?P<least_digit>\d+)($|\.X)', to_version)
        if to_version.__contains__('X'):
            least_digit = int(regex.group('least_digit')) + 1
            x_flag = True
        else:
            least_digit = int(regex.group('least_digit'))
            x_flag = False
        to_version = regex.group('base') + '.' + str(least_digit)
        if (parse_version(from_version) <= parse_version(num_version) <= parse_version(to_version) and x_flag is False)\
                or (parse_version(from_version) <= parse_version(num_version) < parse_version(to_version)
                    and x_flag is True):
            return True
        else:
            return False
    except AttributeError:
        return False

