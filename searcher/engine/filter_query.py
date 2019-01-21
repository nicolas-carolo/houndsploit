from pkg_resources import parse_version
from searcher.engine.version_comparator import get_num_version_with_comparator, get_num_version,\
    is_in_version_range_with_x, is_equal_with_x, is_in_version_range, is_lte_with_comparator_x
from searcher.engine.string import str_contains_num_version_range_with_x, str_contains_num_version_range


def filter_exploits_without_comparator(exploit, num_version, software_name, queryset):
    if not exploit.description.__contains__('.x'):
        # exclude the exploit from results table if the number of version is not equal and contains 'x'
        try:
            if parse_version(num_version) != parse_version(get_num_version(software_name, exploit.description)):
                queryset = queryset.exclude(description__exact=exploit.description)
        except TypeError:
            queryset = queryset.exclude(description__exact=exploit.description)
    else:
        # exclude the exploit from results table if the number of version is not equal and not contains 'x'
        try:
            if not is_equal_with_x(num_version, get_num_version(software_name, exploit.description)):
                queryset = queryset.exclude(description__exact=exploit.description)
        except TypeError:
            queryset = queryset.exclude(description__exact=exploit.description)
    return queryset


def filter_exploits_with_comparator(exploit, num_version, software_name, queryset):
    if not exploit.description.__contains__('.x'):
        queryset = filter_exploits_with_comparator_and_without_x(exploit, num_version, software_name, queryset)
    else:
        queryset = filter_exploits_with_comparator_and_x(exploit, num_version, software_name, queryset)
    return queryset


def filter_shellcodes_without_comparator(shellcode, num_version, software_name, queryset):
    if not shellcode.description.__contains__('.x'):
        # exclude the shellcode from results table if the number of version is not equal and contains 'x'
        try:
            if parse_version(num_version) != parse_version(get_num_version(software_name, shellcode.description)):
                queryset = queryset.exclude(description__exact=shellcode.description)
        except TypeError:
            queryset = queryset.exclude(description__exact=shellcode.description)
    else:
        # exclude the shellcode from results table if the number of version is not equal and not contains 'x'
        try:
            if not is_equal_with_x(num_version, get_num_version(software_name, shellcode.description)):
                queryset = queryset.exclude(description__exact=shellcode.description)
        except TypeError:
            queryset = queryset.exclude(description__exact=shellcode.description)
    return queryset


def filter_shellcodes_with_comparator(shellcode, num_version, software_name, queryset):
    if not shellcode.description.__contains__('.x'):
        queryset = filter_shellcodes_with_comparator_and_without_x(shellcode, num_version, software_name, queryset)
    else:
        queryset = filter_exploits_with_comparator_and_x(shellcode, num_version, software_name, queryset)
    return queryset


def filter_exploits_with_comparator_and_without_x(exploit, num_version, software_name, queryset):
    if str_contains_num_version_range(str(exploit.description)):
        if not is_in_version_range(num_version, software_name, exploit.description):
            queryset = queryset.exclude(description__exact=exploit.description)
    else:
        try:
            if parse_version(num_version) > parse_version(
                    get_num_version_with_comparator(software_name, exploit.description)):
                queryset = queryset.exclude(description__exact=exploit.description)
        except TypeError:
            queryset = queryset.exclude(description__exact=exploit.description)
    return queryset


def filter_exploits_with_comparator_and_x(exploit, num_version, software_name, queryset):
    if str_contains_num_version_range_with_x(str(exploit.description)):
        if not is_in_version_range_with_x(num_version, software_name, exploit.description):
            queryset = queryset.exclude(description__exact=exploit.description)
    else:
        try:
            if not is_lte_with_comparator_x(num_version, software_name, exploit.description):
                queryset = queryset.exclude(description__exact=exploit.description)
        except TypeError:
            queryset = queryset.exclude(description__exact=exploit.description)
    return queryset


def filter_shellcodes_with_comparator_and_without_x(shellcode, num_version, software_name, queryset):
    if str_contains_num_version_range(str(shellcode.description)):
        if not is_in_version_range(num_version, software_name, shellcode.description):
            queryset = queryset.exclude(description__exact=shellcode.description)
    else:
        try:
            if parse_version(num_version) > parse_version(
                    get_num_version_with_comparator(software_name, shellcode.description)):
                queryset = queryset.exclude(description__exact=shellcode.description)
        except TypeError:
            queryset = queryset.exclude(description__exact=shellcode.description)
    return queryset


def filter_shellcodes_with_comparator_and_x(shellcode, num_version, software_name, queryset):
    if str_contains_num_version_range_with_x(str(shellcode.description)):
        if not is_in_version_range_with_x(num_version, software_name, shellcode.description):
            queryset = queryset.exclude(description__exact=shellcode.description)
    else:
        try:
            if not is_lte_with_comparator_x(num_version, software_name, shellcode.description):
                queryset = queryset.exclude(description__exact=shellcode.description)
        except TypeError:
            queryset = queryset.exclude(description__exact=shellcode.description)
    return queryset
