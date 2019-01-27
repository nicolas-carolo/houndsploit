from functools import reduce
from searcher.models import Exploit, Shellcode
from django.db.models import Q
import operator
from searcher.engine.string import str_is_num_version
from searcher.engine.keywords_highlighter import highlight_keywords_in_description, highlight_keywords_in_file, \
    highlight_keywords_in_author, highlight_keywords_in_port
from searcher.engine.filter_query import filter_exploits_with_comparator, filter_exploits_without_comparator, \
    filter_shellcodes_with_comparator, filter_shellcodes_without_comparator

N_MAX_RESULTS_NUMB_VERSION = 20000


def search_vulnerabilities_in_db(search_text, db_table):
    """
    Return the queryset containing search results with keywords highlighted.
    :param search_text: the vulnerability that the user is searching for.
    :param db_table: the DB table in which we want to perform the search.
    :return: a queryset containing search results with keywords highlighted.
    """
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
    """
    Perform a search based on vulnerabilities' description, file, id, and port (only if it is an exploit) for an only
    numerical search input.
    :param search_text: the search input.
    :param db_table: the DB table in which we want to perform the search.
    :return: a queryset with search results.
    """
    if db_table == 'searcher_exploit':
        return Exploit.objects.filter(
            Q(id__exact=int(search_text)) | Q(file__contains=search_text) | Q(description__contains=search_text) | Q(
                port__exact=int(search_text)))
    else:
        return Shellcode.objects.filter(
            Q(id__exact=int(search_text)) | Q(file__contains=search_text) | Q(description__contains=search_text))


def search_vulnerabilities_for_description(search_text, db_table):
    """
    Perform a search based on vulnerabilities' description for an input search that does not contain a number
    of version.
    :param search_text: the search input.
    :param db_table: the DB table in which we want to perform the search.
    :return: a queryset with search results.
    """
    words_list = str(search_text).split()
    query = reduce(operator.and_, (Q(description__icontains=word) for word in words_list))
    if db_table == 'searcher_exploit':
        queryset = Exploit.objects.filter(query)
    else:
        queryset = Shellcode.objects.filter(query)
    return queryset


def search_vulnerabilities_for_file(search_text, db_table):
    """
    Perform a search based on vulnerabilities' file for an input search that does not contain a number of version.
    :param search_text: the search input.
    :param db_table: the DB table in which we want to perform the search.
    :return: a queryset with search results.
    """
    words_list = str(search_text).split()
    query = reduce(operator.or_, (Q(file__icontains=word) for word in words_list))
    if db_table == 'searcher_exploit':
        queryset = Exploit.objects.filter(query)
    else:
        queryset = Shellcode.objects.filter(query)
    return queryset


def search_vulnerabilities_for_author(search_text, db_table):
    """
    Perform a search based on vulnerabilities' author for an input search that does not contain a number of version.
    :param search_text: the search input.
    :param db_table: the DB table in which we want to perform the search.
    :return: a queryset with search results.
    """
    words_list = str(search_text).split()
    query = reduce(operator.and_, (Q(author__icontains=word) for word in words_list))
    if db_table == 'searcher_exploit':
        queryset = Exploit.objects.filter(query)
    else:
        queryset = Shellcode.objects.filter(query)
    return queryset


def search_vulnerabilities_version(search_text, db_table):
    """
    Perform a search based on vulnerabilities' description for an input search that contains a number of version.
    :param search_text: the search input containing also the number of version.
    :param db_table: the DB table in which we want to perform the search.
    :return: a queryset with search results.
    """
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
    """
    Perform a search based on exploits' description for an input search that contains a number of version.
    This function is called by 'search_vulnerabilities_version' method.
    :param software_name: the name of the software that the user is searching for.
    :param num_version: the specific number of version the user is searching for.
    :return: a queryset with search result found in 'searcher_exploit' DB table.
    """
    queryset = Exploit.objects.filter(description__icontains=software_name)
    # limit the time spent for searching useless results.
    if queryset.count() > N_MAX_RESULTS_NUMB_VERSION:
        return Exploit.objects.none()
    for exploit in queryset:
        # if exploit not contains '<'
        if not str(exploit.description).__contains__('<'):
            queryset = filter_exploits_without_comparator(exploit, num_version, software_name, queryset)
        # if exploit contains '<'
        else:
            queryset = filter_exploits_with_comparator(exploit, num_version, software_name, queryset)
    return queryset


def search_shellcodes_version(software_name, num_version):
    """
    Perform a search based on shellcodes' description for an input search that contains a number of version.
    This function is called by 'search_vulnerabilities_version' method.
    :param software_name: the name of the software that the user is searching for.
    :param num_version: the specific number of version the user is searching for.
    :return: a queryset with search result found in 'searcher_shellcode' DB table.
    """
    queryset = Shellcode.objects.filter(description__icontains=software_name)
    # limit the time spent for searching useless results.
    if queryset.count() > N_MAX_RESULTS_NUMB_VERSION:
        return Shellcode.objects.none()
    for shellcode in queryset:
        # if shellcode not contains '<'
        if not str(shellcode.description).__contains__('<'):
            queryset = filter_shellcodes_without_comparator(shellcode, num_version, software_name, queryset)
        # if shellcode contains '<'
        else:
            queryset = filter_shellcodes_with_comparator(shellcode, num_version, software_name, queryset)
    return queryset


def search_vulnerabilities_advanced(search_text, db_table, operator_filter, type_filter, platform_filter, author_filter,
                                    port_filter, start_date_filter, end_date_filter):
    """
    Perform a search based on filter selected by the user for an input search.
    :param search_text: the search input.
    :param db_table: the DB table in which we want to perform the search.
    :param operator_filter: OR operator matches all search results that contain at least one search keyword,
                            AND operator matches only search results that contain all the search keywords.
    :param type_filter: the filter on the vulnerabilities' type.
    :param platform_filter: the filter on the vulnerabilities' platform.
    :param author_filter: the filter on the vulnerabilities' author.
    :param port_filter: the filter on the exploits' port.
    :param start_date_filter: the filter on the vulnerabilities' date (from).
    :param end_date_filter: the filter on the vulnerabilities' date (to).
    :return: a queryset containing all the search results.
    """
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
        queryset = queryset.filter(type__exact=type_filter)
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
    elif port_filter is not None and db_table == 'searcher_shellcode':
        queryset = Shellcode.objects.none()

    queryset_std = search_vulnerabilities_for_text_input_advanced(search_text, db_table, type_filter, platform_filter,
                                                                  author_filter, port_filter, start_date_filter,
                                                                  end_date_filter)
    queryset = queryset.union(queryset_std)

    return highlight_keywords_in_description(words_list, queryset)


def search_vulnerabilities_for_description_advanced(search_text, db_table):
    """
    If the search input contains a number of version, it calls 'search_vulnerabilities_version' method,
    else it calls 'search_vulnerabilities_for_description'.
    :param search_text: the search input.
    :param db_table: the DB table in which we want to perform the search.
    :return: a queryset containing all the search results that can be filtered with the filters selected by the user.
    """
    if str_is_num_version(str(search_text)) and str(search_text).__contains__(' ') \
            and not str(search_text).__contains__('<'):
        queryset = search_vulnerabilities_version(search_text, db_table)
    else:
        queryset = search_vulnerabilities_for_description(search_text, db_table)
    return queryset


def search_vulnerabilities_for_text_input(search_text, db_table):
    """
    Perform a search in description based on characters contained by this attribute.
    This queryset can be joined with the search results based on the number of version.
    :param search_text: the search input.
    :param db_table: the DB table in which we want to perform the search.
    :return: a queryset containing the search results found with a search based on the characters contained by
                the attribute 'description'
    """
    if db_table == 'searcher_exploit':
        queryset = Exploit.objects.filter(description__icontains=search_text)
    else:
        queryset = Shellcode.objects.filter(description__icontains=search_text)
    return queryset


def search_vulnerabilities_for_text_input_advanced(search_text, db_table, type_filter, platform_filter, author_filter,
                                                   port_filter, start_date_filter, end_date_filter):
    """
    Perform a search based on characters contained by this attribute.
    :param search_text: the search input.
    :param db_table: the DB table in which we want to perform the search.
    :param type_filter: the filter on the vulnerabilities' type.
    :param platform_filter: the filter on the vulnerabilities' platform.
    :param author_filter: the filter on the vulnerabilities' author.
    :param port_filter: the filter on the exploits' port.
    :param start_date_filter: the filter on the vulnerabilities' date (from).
    :param end_date_filter: the filter on the vulnerabilities' date (to).
    :return: a queryset containing all the search results.
    """
    if db_table == 'searcher_exploit':
        queryset = Exploit.objects.filter(description__icontains=search_text)
    else:
        queryset = Shellcode.objects.filter(description__icontains=search_text)

    if type_filter != 'All':
        queryset = queryset.filter(type__exact=type_filter)
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
    elif port_filter is not None and db_table == 'searcher_shellcode':
        queryset = Shellcode.objects.none()
    return queryset
