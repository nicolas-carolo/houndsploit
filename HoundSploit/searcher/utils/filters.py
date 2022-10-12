import datetime
from pkg_resources import parse_version
from HoundSploit.searcher.engine.version_comparator import get_num_version_with_comparator, get_num_version_without_comparator,\
    is_in_version_range_with_x, is_equal_with_x, is_in_version_range_without_x, is_lte_with_comparator_x
from HoundSploit.searcher.utils.string import str_contains_num_version_range_with_x, str_contains_num_version_range


def filter_vulnerabilities_without_comparator(vulnerability, num_version, software_name, final_result_set):
    if not vulnerability.description.__contains__('.x'):
        # exclude the vulnerability from results table if the number of version is not equal and contains 'x'
        try:
            if parse_version(num_version) == parse_version(get_num_version_without_comparator(software_name, vulnerability.description)):
                final_result_set.append(vulnerability)
        except TypeError:
            pass
    else:
        # exclude the vulnerability from results table if the number of version is not equal and not contains 'x'
        try:
            if is_equal_with_x(num_version, get_num_version_without_comparator(software_name, vulnerability.description)):
                final_result_set.append(vulnerability)
        except TypeError:
            pass
    return final_result_set


def filter_vulnerabilities_with_comparator(vulnerability, num_version, software_name, final_result_set):
    if not vulnerability.description.__contains__('.x'):
        final_result_set = filter_vulnerabilities_with_comparator_and_without_x(vulnerability, num_version, software_name, final_result_set)
    else:
        final_result_set = filter_vulnerabilities_with_comparator_and_x(vulnerability, num_version, software_name, final_result_set)
    return final_result_set


def filter_vulnerabilities_with_comparator_and_without_x(vulnerability, num_version, software_name, final_result_set):
    if str_contains_num_version_range(str(vulnerability.description)):
        if is_in_version_range_without_x(num_version, software_name, vulnerability.description):
            final_result_set.append(vulnerability)
    else:
        try:
            if parse_version(num_version) <= parse_version(
                    get_num_version_with_comparator(software_name, vulnerability.description)):
                final_result_set.append(vulnerability)
        except TypeError:
            pass
    return final_result_set


def filter_vulnerabilities_with_comparator_and_x(vulnerability, num_version, software_name, final_result_set):
    if str_contains_num_version_range_with_x(str(vulnerability.description)):
        if is_in_version_range_with_x(num_version, software_name, vulnerability.description):
            final_result_set.append(vulnerability)
    else:
        try:
            if is_lte_with_comparator_x(num_version, software_name, vulnerability.description):
                final_result_set.append(vulnerability)
        except TypeError:
            pass
    return final_result_set