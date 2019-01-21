from functools import reduce
from searcher.models import Exploit, Shellcode
import re
from django.db.models import Q
import operator
from pkg_resources import parse_version


def search_vulnerabilities_in_db(search_text, db_table):
    words = (str(search_text).upper()).split()
    if str(search_text).isnumeric():
        queryset = search_vulnerabilities_numerical(search_text, db_table)
        queryset = highlight_keywords_in_file(words, queryset)
        queryset = highlight_keywords_in_description(words, queryset)
        if db_table == 'searcher_exploit':
            queryset = highlight_keywords_in_port(words, queryset)
        return queryset
    elif str_is_num_version(str(search_text)) and str(search_text).__contains__(' ') and not str(
            search_text).__contains__('<'):
        queryset = search_vulnerabilities_version(search_text, db_table)
        # union with standard research (test)
        queryset_std = search_vulnerabilities_for_text_input(search_text, db_table)
        queryset = queryset.union(queryset_std)
        return highlight_keywords_in_description(words, queryset)
    else:
        queryset = search_vulnerabilities_for_description(search_text, db_table)
        if len(queryset) > 0:
            return highlight_keywords_in_description(words, queryset)
        else:
            queryset = search_vulnerabilities_for_file(search_text, db_table)
            if len(queryset) > 0:
                return highlight_keywords_in_file(words, queryset)
            else:
                queryset = search_vulnerabilities_for_author(search_text, db_table)
                return highlight_keywords_in_author(words, queryset)


def search_vulnerabilities_numerical(search_text, db_table):
    if db_table == 'searcher_exploit':
        return Exploit.objects.filter(
            Q(id__exact=int(search_text)) | Q(file__contains=search_text) | Q(description__contains=search_text) | Q(
                port__exact=int(search_text)))
    else:
        return Shellcode.objects.filter(
            Q(id__exact=int(search_text)) | Q(file__contains=search_text) | Q(description__contains=search_text))


def search_vulnerabilities_for_description(search_text, db_table):
    # I have installed reduce
    words_list = str(search_text).split()
    query = reduce(operator.and_, (Q(description__icontains=word) for word in words_list))
    if db_table == 'searcher_exploit':
        queryset = Exploit.objects.filter(query)
    else:
        queryset = Shellcode.objects.filter(query)
    return queryset


def search_vulnerabilities_for_file(search_text, db_table):
    words_list = str(search_text).split()
    query = reduce(operator.or_, (Q(file__icontains=word) for word in words_list))
    if db_table == 'searcher_exploit':
        queryset = Exploit.objects.filter(query)
    else:
        queryset = Shellcode.objects.filter(query)
    return queryset


def search_vulnerabilities_for_author(search_text, db_table):
    words_list = str(search_text).split()
    query = reduce(operator.and_, (Q(author__icontains=word) for word in words_list))
    if db_table == 'searcher_exploit':
        queryset = Exploit.objects.filter(query)
    else:
        queryset = Shellcode.objects.filter(query)
    return queryset


def str_contains_numbers(str):
    return bool(re.search(r'\d', str))


def str_is_num_version(str):
    return bool(re.search(r'\d+((\.\d+)+)?', str))


def str_contains_num_version_range(str):
    return bool(re.search(r'\d+((\.\d+)+)? < \d+((\.\d+)+)?', str))


def str_contains_num_version_range_with_x(str):
    return bool(re.search(r'\d+((\.\d+)+)?(\.x)? < \d+((\.\d+)+)?(\.x)?', str))


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
    version_precision = str(num_to_compare).count('.') + 1
    try:
        if version_precision == 1:
            regex = re.search(r'\d+', num_version)
        elif version_precision == 2:
            regex = re.search(r'\d+\.\d+', num_version)
        elif version_precision == 3:
            regex = re.search(r'\d+\.\d+\.\d+', num_version)
        elif version_precision == 4:
            regex = re.search(r'\d+\.\d+\.\d+\.\d+', num_version)
        num_version = regex.group()
    except AttributeError:
        pass
    if parse_version(num_version) == parse_version(num_to_compare):
        return True
    else:
        return False


def search_vulnerabilities_version(search_text, db_table):
    words = str(search_text).upper().split()
    software_name = words[0]
    for word in words[1:]:
        if not str_is_num_version(word):
            software_name = software_name + ' ' + word
        else:
            num_version = word
    if db_table == 'searcher_exploit':
        return search_exploits_version(software_name, num_version)
    else:
        return search_shellcodes_version(software_name, num_version)


def search_exploits_version(software_name, num_version):
    queryset = Exploit.objects.filter(description__icontains=software_name)
    for exploit in queryset:
        # if exploit not contains '<'
        if not str(exploit.description).__contains__('<'):
            queryset = filter_exploits_without_comparator(exploit, num_version, software_name, queryset)
        # if exploit contains '<'
        else:
            queryset = filter_exploits_with_comparator(exploit, num_version, software_name, queryset)
    return queryset


def search_shellcodes_version(software_name, num_version):
    queryset = Shellcode.objects.filter(description__icontains=software_name)
    for shellcode in queryset:
        # if shellcode not contains '<'
        if not str(shellcode.description).__contains__('<'):
            queryset = filter_shellcodes_without_comparator(shellcode, num_version, software_name, queryset)
        # if shellcode contains '<'
        else:
            queryset = filter_shellcodes_with_comparator(shellcode, num_version, software_name, queryset)
    return queryset


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


def highlight_keywords_in_description(keywords_list, queryset):
    for vulnerability in queryset:
        for keyword in keywords_list:
            if keyword != '<':
                description = str(vulnerability.description).upper()
                if description.__contains__(keyword):
                    regex = re.compile(re.escape(keyword), re.IGNORECASE)
                    vulnerability.description = regex.sub("<span class='keyword'>" + keyword + '</span>',
                                                          vulnerability.description)
    return queryset


def highlight_keywords_in_file(keywords_list, queryset):
    for vulnerability in queryset:
        for keyword in keywords_list:
            file = str(vulnerability.file).upper()
            if file.__contains__(keyword):
                regex = re.compile(re.escape(keyword), re.IGNORECASE)
                vulnerability.file = regex.sub("<span class='keyword'>" + keyword + '</span>', vulnerability.file)
    return queryset


def highlight_keywords_in_author(keywords_list, queryset):
    for vulnerability in queryset:
        for keyword in keywords_list:
            file = str(vulnerability.author).upper()
            if file.__contains__(keyword):
                regex = re.compile(re.escape(keyword), re.IGNORECASE)
                vulnerability.author = regex.sub("<span class='keyword'>" + keyword + '</span>', vulnerability.author)
    return queryset


def highlight_keywords_in_port(keywords_list, queryset):
    for exploit in queryset:
        for keyword in keywords_list:
            file = str(exploit.port).upper()
            if file.__contains__(keyword):
                regex = re.compile(re.escape(keyword), re.IGNORECASE)
                exploit.port = regex.sub("<span class='keyword'>" + keyword + '</span>', exploit.port)
    return queryset


def search_vulnerabilities_advanced(search_text, db_table, operator_filter, type_filter, platform_filter, author_filter, port_filter, start_date_filter, end_date_filter):
    words_list = str(search_text).upper().split()
    if operator_filter == 'AND' and search_text != '':
        queryset = search_vulnerabilities_for_description_advanced(search_text, db_table)
    elif operator_filter == 'OR':
        try:
            query = reduce(operator.or_, (Q(description__icontains=word) for word in words_list))
            if db_table == 'searcher_exploit':
                queryset = Exploit.objects.filter(query)
            else:
                queryset = Shellcode.objects.filter(query)
        except TypeError:
            if db_table == 'searcher_exploit':
                queryset = Exploit.objects.all()
            else:
                queryset = Shellcode.objects.all()
    else:
        if db_table == 'searcher_exploit':
            queryset = Exploit.objects.all()
        else:
            queryset = Shellcode.objects.all()
    if type_filter != 'All':
        queryset = queryset.filter(vulnerability_type__exact=type_filter)
    if platform_filter != 'All':
        queryset = queryset.filter(platform__exact=platform_filter)
    if author_filter != '':
        queryset = queryset.filter(author__icontains=author_filter)
    try:
        queryset = queryset.filter(date__gte=start_date_filter)
        queryset = queryset.filter(date__lte=end_date_filter)
    except ValueError:
        pass
    if port_filter is not None and db_table == 'searcher_exploit':
        queryset = queryset.filter(port__exact=port_filter)
        return highlight_keywords_in_description(words_list, queryset)
    elif port_filter is not None and db_table == 'searcher_shellcode':
        return Shellcode.objects.none()
    else:
        return highlight_keywords_in_description(words_list, queryset)


def search_vulnerabilities_for_description_advanced(search_text, db_table):
    if str_is_num_version(str(search_text)) and str(search_text).__contains__(' ') and not str(search_text).__contains__('<'):
        queryset = search_vulnerabilities_version(search_text, db_table)
    else:
        queryset = search_vulnerabilities_for_description(search_text, db_table)
    return queryset


def search_vulnerabilities_for_text_input(search_text, db_table):
    if db_table == 'searcher_exploit':
        queryset = Exploit.objects.filter(description__icontains=search_text)
    else:
        queryset = Shellcode.objects.filter(description__icontains=search_text)
    return queryset
