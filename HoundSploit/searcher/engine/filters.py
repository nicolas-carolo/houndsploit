import datetime
from pkg_resources import parse_version
from HoundSploit.searcher.engine.version_comparator import get_num_version_with_comparator, get_num_version,\
    is_in_version_range_with_x, is_equal_with_x, is_in_version_range, is_lte_with_comparator_x
from HoundSploit.searcher.utils.string import str_contains_num_version_range_with_x, str_contains_num_version_range


def filter_vulnerabilities(vulnerabilities_list, filters):
    if filters["type"] != 'all':
        vulnerabilities_list = filter_vulnerabilities_for_type(vulnerabilities_list, filters["type"])
    if filters["platform"] != 'all':
        vulnerabilities_list = filter_vulnerabilities_for_platform(vulnerabilities_list, filters["platform"])
    if filters["author"] != '':
        vulnerabilities_list = filter_vulnerabilities_for_author(vulnerabilities_list, filters["author"])
    try:
        date_from = datetime.datetime.strptime(filters["date_from"], '%Y-%m-%d')
        date_to = datetime.datetime.strptime(filters["date_to"], '%Y-%m-%d')
        vulnerabilities_list = filter_vulnerabilities_for_date_range(vulnerabilities_list, date_from, date_to)
    except ValueError:
        pass
    if filters["port"] != '':
        vulnerabilities_list = filter_exploits_for_port(vulnerabilities_list, filters["port"])
    return vulnerabilities_list


def filter_vulnerabilities_for_author(vulnerabilities_list, author_filter):
    output_list = []
    for vulnerability in vulnerabilities_list:
        if vulnerability.author == author_filter:
            output_list.append(vulnerability)
    return output_list


def filter_vulnerabilities_for_type(vulnerabilities_list, type_filter):
    output_list = []
    for vulnerability in vulnerabilities_list:
        if vulnerability.type == type_filter:
            output_list.append(vulnerability)
    return output_list


def filter_vulnerabilities_for_platform(vulnerabilities_list, platform_filter):
    output_list = []
    for vulnerability in vulnerabilities_list:
        if vulnerability.platform == platform_filter:
            output_list.append(vulnerability)
    return output_list


def filter_exploits_for_port(vulnerabilities_list, port_filter):
    output_list = []
    for vulnerability in vulnerabilities_list:
        try:
            if vulnerability.port == port_filter:
                output_list.append(vulnerability)
        except AttributeError:
            pass
    return output_list


def filter_vulnerabilities_for_date_range(vulnerabilities_list, date_from, date_to):
    output_list = []
    for vulnerability in vulnerabilities_list:
        vulnerability_date = datetime.datetime.strptime(vulnerability.date, '%Y-%m-%d')
        if date_from <= vulnerability_date <= date_to:
            output_list.append(vulnerability)
    return output_list
