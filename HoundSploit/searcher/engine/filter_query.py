from pkg_resources import parse_version
from HoundSploit.searcher.engine.version_comparator import get_num_version_with_comparator, get_num_version,\
    is_in_version_range_with_x, is_equal_with_x, is_in_version_range, is_lte_with_comparator_x
from HoundSploit.searcher.engine.string import str_contains_num_version_range_with_x, str_contains_num_version_range
import datetime


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

