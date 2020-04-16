from pkg_resources import parse_version
from HoundSploit.searcher.engine.version_comparator import get_num_version_with_comparator, get_num_version,\
    is_in_version_range_with_x, is_equal_with_x, is_in_version_range, is_lte_with_comparator_x
from HoundSploit.searcher.engine.string import str_contains_num_version_range_with_x, str_contains_num_version_range
import datetime


def filter_exploits_without_comparator(exploit, num_version, software_name, final_result_set):
    """
    Add the exploit (without comparator) to the final_result_set if respect the condition set by the user.
    :param exploit: the exploit we have to check if it has a number of version that matches the value passed by
                    the user.
    :param num_version: the number of version searched by the user.
    :param software_name: the name of the software searched by the user.
    :param final_result_set: the result set that
    :return: the result set that
    """
    if not exploit.description.__contains__('.x'):
        # exclude the exploit from results table if the number of version is not equal and contains 'x'
        try:
            if parse_version(num_version) == parse_version(get_num_version(software_name, exploit.description)):
                final_result_set.append(exploit)
        except TypeError:
            pass
    else:
        # exclude the exploit from results table if the number of version is not equal and not contains 'x'
        try:
            if is_equal_with_x(num_version, get_num_version(software_name, exploit.description)):
                final_result_set.append(exploit)
        except TypeError:
            pass
    return final_result_set


def filter_exploits_with_comparator(exploit, num_version, software_name, final_result_set):
    """
    Add the exploit (with comparator) to the final_result_set if respect the condition set by the user.
    :param exploit: the exploit we have to check if it has a number of version that matches the value passed by
                    the user.
    :param num_version: the number of version searched by the user.
    :param software_name: the name of the software searched by the user.
    :param final_result_set: the result set that
    :return: the result set that
    """
    if not exploit.description.__contains__('.x'):
        final_result_set = filter_exploits_with_comparator_and_without_x(exploit, num_version, software_name, final_result_set)
    else:
        final_result_set = filter_exploits_with_comparator_and_x(exploit, num_version, software_name, final_result_set)
    return final_result_set


def filter_exploits_with_comparator_and_without_x(exploit, num_version, software_name, final_result_set):
    """
    Add exploit (with comparator and without the x in number version) to the final_result_set if respect the condition set by the user.
    :param exploit: the exploit we have to check if it has a number of version that matches the value passed by
                    the user.
    :param num_version: the number of version searched by the user.
    :param software_name: the name of the software searched by the user.
    :param final_result_set: the result set that
    :return: the result set that
    """
    if str_contains_num_version_range(str(exploit.description)):
        if is_in_version_range(num_version, software_name, exploit.description):
            final_result_set.append(exploit)
    else:
        try:
            if parse_version(num_version) <= parse_version(
                    get_num_version_with_comparator(software_name, exploit.description)):
                final_result_set.append(exploit)
        except TypeError:
            pass
    return final_result_set


def filter_exploits_with_comparator_and_x(exploit, num_version, software_name, final_result_set):
    """
    Add exploit (with comparator and x in the number version) to the final_result_set if respect the condition set by the user.
    :param exploit: the exploit we have to check if it has a number of version that matches the value passed by
                    the user.
    :param num_version: the number of version searched by the user.
    :param software_name: the name of the software searched by the user.
    :param final_result_set: the result set that
    :return: the result set that
    """
    if str_contains_num_version_range_with_x(str(exploit.description)):
        if is_in_version_range_with_x(num_version, software_name, exploit.description):
            final_result_set.append(exploit)
    else:
        try:
            if is_lte_with_comparator_x(num_version, software_name, exploit.description):
                final_result_set.append(exploit)
        except TypeError:
            pass
    return final_result_set


def filter_shellcodes_without_comparator(shellcode, num_version, software_name, final_result_set):
    """
    Add the shellcode (without comparator) to the final_result_set if respect the condition set by the user.
    :param shellcode: the shellcode we have to check if it has a number of version that matches the value passed by
                        the user.
    :param num_version: the number of version searched by the user.
    :param software_name: the name of the software searched by the user.
    :param final_result_set: the result set that
    :return: the result set that
    """
    if not shellcode.description.__contains__('.x'):
        # exclude the exploit from results table if the number of version is not equal and contains 'x'
        try:
            if parse_version(num_version) == parse_version(get_num_version(software_name, shellcode.description)):
                final_result_set.append(shellcode)
        except TypeError:
            pass
    else:
        # exclude the exploit from results table if the number of version is not equal and not contains 'x'
        try:
            if is_equal_with_x(num_version, get_num_version(software_name, shellcode.description)):
                final_result_set.append(shellcode)
        except TypeError:
            pass
    return final_result_set


def filter_shellcodes_with_comparator(shellcode, num_version, software_name, final_result_set):
    """
    Add the shellcode (with comparator) to the final_result_set if respect the condition set by the user.
    :param shellcode: the shellcode we have to check if it has a number of version that matches the value passed by
                        the user.
    :param num_version: the number of version searched by the user.
    :param software_name: the name of the software searched by the user.
    :param final_result_set: the result set that
    :return: the result set that
    """
    if not shellcode.description.__contains__('.x'):
        final_result_set = filter_shellcodes_with_comparator_and_without_x(shellcode, num_version, software_name, final_result_set)
    else:
        final_result_set = filter_shellcodes_with_comparator_and_x(shellcode, num_version, software_name, final_result_set)
    return final_result_set


def filter_shellcodes_with_comparator_and_without_x(shellcode, num_version, software_name, final_result_set):
    """
    Add the shellcode (with comparator and without x) to the final_result_set if respect the condition set by the user.
    :param shellcode: the shellcode we have to check if it has a number of version that matches the value passed by
                        the user.
    :param num_version: the number of version searched by the user.
    :param software_name: the name of the software searched by the user.
    :param final_result_set: the result set that
    :return: the result set that
    """
    if str_contains_num_version_range(str(shellcode.description)):
        if is_in_version_range(num_version, software_name, shellcode.description):
            final_result_set.append(shellcode)
    else:
        try:
            if parse_version(num_version) <= parse_version(
                    get_num_version_with_comparator(software_name, shellcode.description)):
                final_result_set.append(shellcode)
        except TypeError:
            pass
    return final_result_set


def filter_shellcodes_with_comparator_and_x(shellcode, num_version, software_name, final_result_set):
    """
    Add the shellcode (with comparator and x) to the final_result_set if respect the condition set by the user.
    :param shellcode: the shellcode we have to check if it has a number of version that matches the value passed by
                        the user.
    :param num_version: the number of version searched by the user.
    :param software_name: the name of the software searched by the user.
    :param final_result_set: the result set that
    :return: the result set that
    """
    if str_contains_num_version_range_with_x(str(shellcode.description)):
        if is_in_version_range_with_x(num_version, software_name, shellcode.description):
            final_result_set.append(shellcode)
    else:
        try:
            if is_lte_with_comparator_x(num_version, software_name, shellcode.description):
                final_result_set.append(shellcode)
        except TypeError:
            pass
    return final_result_set


def filter_vulnerabilities_for_author(input_list, author_filter):
    output_list = []
    for vulnerability in input_list:
        if vulnerability.author == author_filter:
            output_list.append(vulnerability)
    return output_list


def filter_vulnerabilities_for_type(input_list, type_filter):
    output_list = []
    for vulnerability in input_list:
        if vulnerability.type == type_filter:
            output_list.append(vulnerability)
    return output_list


def filter_vulnerabilities_for_platform(input_list, platform_filter):
    output_list = []
    for vulnerability in input_list:
        if vulnerability.platform == platform_filter:
            output_list.append(vulnerability)
    return output_list


def filter_exploits_for_port(input_list, port_filter):
    output_list = []
    for vulnerability in input_list:
        if vulnerability.port == port_filter:
            output_list.append(vulnerability)
    return output_list


def filter_vulnerabilities_for_date_range(input_list, date_from, date_to):
    output_list = []
    for vulnerability in input_list:
        if date_from < datetime.datetime.strptime(vulnerability.date, '%Y-%m-%d') < date_to:
            output_list.append(vulnerability)
    return output_list

