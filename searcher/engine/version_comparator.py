import re
from pkg_resources import parse_version


def get_num_version(software_name, description):
    software_name = software_name.upper()
    description = description.upper()
    regex = re.search(software_name + r' \d+((\.\d+)+)?', description)
    try:
        software = regex.group(0)
        regex = re.search(r'\d+((\.\d+)+)?', software)
        try:
            return regex.group(0)
        except AttributeError:
            return
    except AttributeError:
        return


def get_num_version_with_comparator(software_name, description):
    software_name = software_name.upper()
    description = description.upper()
    regex = re.search(software_name + r' < \d+((\.\d+)+)?', description)
    try:
        software = regex.group(0)
        regex = re.search(r'\d+((\.\d+)+)?', software)
        try:
            return regex.group(0)
        except AttributeError:
            return
    except AttributeError:
        return


def is_lte_with_comparator_x(num_version, software_name, description):
    software_name = software_name.upper()
    description = description.upper()
    regex = re.search(software_name + r' < \d+((\.\d+)+)?', description)
    try:
        software = regex.group(0)
        regex = re.search(r'\d+((\.\d+)+)?', software)
        try:
            num_to_compare = regex.group(0)
            version_precision = str(num_to_compare).count('.')
        except AttributeError:
            return False
    except AttributeError:
        return False
    try:
        regex = re.search(r'\d+(\.\d+){0,%d}' % version_precision, num_version)
        num_version = regex.group()
    except AttributeError:
        return False
    if parse_version(num_version) <= parse_version(num_to_compare):
        return True
    else:
        return False


def is_in_version_range(num_version, software_name, description):
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
        regex = re.search(r'(?P<base>\w+)\.(?P<least_digit>\d+)($|\.X)', to_version)
        if to_version.__contains__('X'):
            least_digit = int(regex.group('least_digit')) + 1
        else:
            least_digit = int(regex.group('least_digit'))
        to_version = regex.group('base') + '.' + str(least_digit)
        if parse_version(num_version) >= parse_version(from_version) and parse_version(
                num_version) < parse_version(to_version):
            return True
        else:
            return False
    except AttributeError:
        return False


def is_equal_with_x(num_version, num_to_compare):
    version_precision = str(num_to_compare).count('.')
    try:
        regex = re.search(r'\d+(\.\d+){0,%d}' % version_precision, num_version)
        num_version = regex.group()
    except AttributeError:
        pass
    if parse_version(num_version) == parse_version(num_to_compare):
        return True
    else:
        return False
