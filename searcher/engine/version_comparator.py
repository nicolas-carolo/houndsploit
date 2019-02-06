import re
from pkg_resources import parse_version


def get_num_version(software_name, description):
    """
    Get the number of the version of the software contained in a description of a vulnerability without '<' char.
    :param software_name: the name of the software we want to get the number of version.
    :param description: the description of the vulnerability from which we want to get the number of the version.
    :return: the number of version if it is possible to get it, None else.
    """
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
    """
    Get the number of the version of the software contained in a description of a vulnerability containing '<' char.
    :param software_name: the name of the software we want to get the number of version.
    :param description: the description of the vulnerability from which we want to get the number of the version.
    :return: the number of version if it is possible to get it, None else.
    """
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
    """
    Check if the vulnerability's description contains the number of version (with comparator and the x) of the software
        searched by the user.
    :param num_version: the number of version searched by the user.
    :param software_name: the name of the software searched by the user.
    :param description: the vulnerability's description to check.
    :return: True if the vulnerability's description contains the number of version of the software searched by
                the user, False else.
    """
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
        print(regex.group('base'))
        print(software, from_version, to_version)
        if (parse_version(from_version) <= parse_version(num_version) <= parse_version(to_version) and x_flag is False)\
                or (parse_version(from_version) <= parse_version(num_version) < parse_version(to_version)
                    and x_flag is True):
            return True
        else:
            return False
    except AttributeError:
        return False


def is_equal_with_x(num_version, num_to_compare):
    """
    Check if the number of version searched by the user is equal to the number of version (with x) of the software
    contained in the vulnerability's description.
    :param num_version: the number of version searched by the user.
    :param num_to_compare: the number of version (containing the x) in the vulnerability's description.
    :return: True if the number of version searched by the user is equal to the number of version (with x) of the
                software contained in the vulnerability's description.
    """
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
