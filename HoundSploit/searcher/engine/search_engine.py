import re
import datetime

from HoundSploit.searcher.engine.string import str_is_num_version, word_is_num_version
from HoundSploit.searcher.engine.filter_query import filter_exploits_without_comparator, filter_exploits_with_comparator,\
    filter_shellcodes_without_comparator, filter_shellcodes_with_comparator

from sqlalchemy import and_, or_
from HoundSploit.searcher.entities.shellcode import Shellcode
from HoundSploit.searcher.entities.exploit import Exploit
from HoundSploit.searcher.db_manager.session_manager import start_session
from HoundSploit.searcher.db_manager.result_set import queryset2list, void_result_set
from HoundSploit.searcher.engine.lists import remove_duplicates_by_list, join_lists
from HoundSploit.searcher.engine.filter_query import filter_vulnerabilities_for_author, filter_vulnerabilities_for_type,\
    filter_vulnerabilities_for_platform, filter_exploits_for_port, filter_vulnerabilities_for_date_range

N_MAX_RESULTS_NUMB_VERSION = 20000


# TODO remove
def search_vulnerabilities_in_db(searched_text, db_table):
    word_list = str(searched_text).split()
    if str(searched_text).isnumeric():
        return search_vulnerabilities_numerical(word_list[0], db_table)
    elif str_is_num_version(str(searched_text)) and str(searched_text).__contains__(' ') and not str(
            searched_text).__contains__('<'):
        result_set = search_vulnerabilities_version(word_list, db_table)
        # union with standard research
        std_result_set = search_vulnerabilities_for_text_input(searched_text, db_table)
        # union_result_set = join_result_sets(result_set, std_result_set, db_table)
        union_result_set = join_lists(queryset2list(result_set), queryset2list(std_result_set))
        if len(union_result_set) > 0:
            return union_result_set
        else:
            return search_vulnerabilities_for_description(word_list, db_table)
    else:
        result_set = search_vulnerabilities_for_description(word_list, db_table)
        if len(result_set) > 0:
            return result_set
        else:
            result_set = search_vulnerabilities_for_file(word_list, db_table)
            if len(result_set) > 0:
                return result_set
            else:
                return search_vulnerabilities_for_author(word_list, db_table)

# TODO remove
def search_vulnerabilities_numerical(searched_text, db_table):
    session = start_session()
    if db_table == 'searcher_exploit':
        queryset = session.query(Exploit).filter(or_(Exploit.description.contains(searched_text),
                                                     Exploit.id == int(searched_text),
                                                     Exploit.file.contains(searched_text),
                                                     Exploit.port == int(searched_text)
                                                     ))
    else:
        queryset = session.query(Shellcode).filter(or_(Shellcode.description.contains(searched_text),
                                                       Shellcode.id == int(searched_text),
                                                       Shellcode.file.contains(searched_text)
                                                       ))
    session.close()
    return queryset2list(queryset)


def search_vulnerabilities_for_description(word_list, db_table):
    """
    Search vulnerabilities for description.
    :param word_list: the list of words searched by the user.
    :param db_table: the database table in which perform the search.
    :return: the list containing the results of the performed search.
    """
    session = start_session()

    if db_table == 'searcher_exploit':
        queryset = session.query(Exploit).filter(and_(Exploit.description.contains(word) for word in word_list))
    else:
        queryset = session.query(Shellcode).filter(
            and_(Shellcode.description.contains(word) for word in word_list))

    session.close()
    return queryset2list(queryset)


def search_vulnerabilities_for_file(word_list, db_table):
    """
    Search vulnerabilities for file.
    :param word_list: the list of words searched by the user.
    :param db_table: the database table in which perform the search.
    :return: the list containing the results of the performed search.
    """
    session = start_session()

    if db_table == 'searcher_exploit':
        queryset = session.query(Exploit).filter(and_(Exploit.file.contains(word) for word in word_list))
    else:
        queryset = session.query(Shellcode).filter(
            and_(Shellcode.file.contains(word) for word in word_list))

    session.close()
    return queryset2list(queryset)


def search_vulnerabilities_for_author(word_list, db_table):
    """
    Search vulnerabilities for author.
    :param word_list: the list of words searched by the user.
    :param db_table: the database table in which perform the search.
    :return: the list containing the results of the performed search.
    """
    session = start_session()

    if db_table == 'searcher_exploit':
        queryset = session.query(Exploit).filter(and_(Exploit.author.contains(word) for word in word_list))
    else:
        queryset = session.query(Shellcode).filter(
            and_(Shellcode.author.contains(word) for word in word_list))

    session.close()
    return queryset2list(queryset)


def search_vulnerabilities_version(word_list, db_table):
    """
    Search vulnerabilities for version number.
    :param word_list: the list of words searched by the user.
    :param db_table: the database table in which perform the search.
    :return: the list containing the results of the performed search.
    """
    software_name = word_list[0]
    for word in word_list[1:]:
        if not word_is_num_version(word):
            software_name = software_name + ' ' + word
        else:
            num_version = word
    if db_table == 'searcher_exploit':
        try:
            return search_exploits_version(software_name, num_version)
        except UnboundLocalError:
            return []
    else:
        try:
            return search_shellcodes_version(software_name, num_version)
        except UnboundLocalError:
            return []


def search_exploits_version(software_name, num_version):
    """
    Perform a search based on exploits' description for an input search that contains a number of version.
    This function is called by 'search_vulnerabilities_version' method.
    :param software_name: the name of the software that the user is searching for.
    :param num_version: the specific number of version the user is searching for.
    :return: a queryset with search result found in 'searcher_exploit' DB table.
    """
    session = start_session()
    queryset = session.query(Exploit).filter(and_(Exploit.description.contains(software_name)))
    query_result_set = queryset2list(queryset)
    session.close()
    # limit the time spent for searching useless results.
    if queryset.count() > N_MAX_RESULTS_NUMB_VERSION:
        return void_result_set()
    final_result_set = []
    for exploit in query_result_set:
        # if exploit not contains '<'
        if not str(exploit.description).__contains__('<'):
            final_result_set = filter_exploits_without_comparator(exploit, num_version, software_name, final_result_set)
        # if exploit contains '<'
        else:
            final_result_set = filter_exploits_with_comparator(exploit, num_version, software_name, final_result_set)
    return final_result_set


def search_shellcodes_version(software_name, num_version):
    """
    Perform a search based on exploits' description for an input search that contains a number of version.
    This function is called by 'search_vulnerabilities_version' method.
    :param software_name: the name of the software that the user is searching for.
    :param num_version: the specific number of version the user is searching for.
    :return: a queryset with search result found in 'searcher_exploit' DB table.
    """
    session = start_session()
    queryset = session.query(Shellcode).filter(and_(Shellcode.description.contains(software_name)))
    query_result_set = queryset2list(queryset)
    session.close()
    # limit the time spent for searching useless results.
    if queryset.count() > N_MAX_RESULTS_NUMB_VERSION:
        # return Exploit.objects.none()
        return void_result_set()
    final_result_set = []
    for shellcode in query_result_set:
        # if exploit not contains '<'
        if not str(shellcode.description).__contains__('<'):
            final_result_set = filter_shellcodes_without_comparator(shellcode, num_version, software_name, final_result_set)
        # if exploit contains '<'
        else:
            final_result_set = filter_shellcodes_with_comparator(shellcode, num_version, software_name, final_result_set)
    return final_result_set


def search_vulnerabilities_for_text_input(searched_text, db_table):
    """
    Perform a search in description based on characters contained by this attribute.
    This queryset can be joined with the search results based on the number of version.
    :param searched_text: the search input.
    :param db_table: the DB table in which we want to perform the search.
    :return: a queryset containing the search results found with a search based on the characters contained by
                the attribute 'description'
    """
    word_list = str(searched_text).split()
    word_list_num = []
    for word in word_list:
        if word.isnumeric():
            word_list.remove(word)
            word_list_num.append(' ' + word)
            word_list_num.append('/' + word)
        if word.__contains__('.'):
            word_list.remove(word)
            word_list_num.append(' ' + word)
            word_list_num.append('/' + word)
    try:
        session = start_session()
        if db_table == 'searcher_exploit':
            queryset = session.query(Exploit).filter(
                and_(Exploit.description.contains(word) for word in word_list))
        else:
            queryset = session.query(Shellcode).filter(
                and_(Shellcode.description.contains(word) for word in word_list))
        session.close()
        query_result_set = queryset2list(queryset)
    except TypeError:
        query_result_set = void_result_set()
    final_result_set = []
    try:
        for instance in query_result_set:
            for word in word_list_num:
                if str(instance.description).__contains__(word) and not list(final_result_set).__contains__(instance):
                    final_result_set.append(instance)
    except TypeError:
        pass
    return final_result_set


def get_exploit_by_id(exploit_id):
    session = start_session()
    exploit = session.query(Exploit).get(exploit_id)
    session.close()
    return exploit


def get_shellcode_by_id(shellcode_id):
    session = start_session()
    shellcode = session.query(Shellcode).get(shellcode_id)
    session.close()
    return shellcode


def get_vulnerability_extension(vulnerability_file):
    """
    Get the extension of the vulnerability passed as parameter.
    :param vulnerability_file: the vulnerability we want to get its extension.
    :return: the extension of the vulnerability passed as parameter.
    """
    regex = re.search(r'\.(?P<extension>\w+)', vulnerability_file)
    extension = '.' + regex.group('extension')
    return extension


def get_vulnerability_filters():
    """
    Get the list of all vulnerability filters
    :return: a list containing all vulnerability types and a list containing all platforms
    """
    session = start_session()
    queryset = session.query(Exploit)
    exploits_list = queryset2list(queryset)
    types_list = []
    platform_list = []
    for exploit in exploits_list:
        types_list.append(exploit.type)
        platform_list.append(exploit.platform)
    queryset = session.query(Shellcode)
    shellcodes_list = queryset2list(queryset)
    for shellcode in shellcodes_list:
        types_list.append(shellcode.type)
        platform_list.append(shellcode.platform)
    types_list = sorted(remove_duplicates_by_list(types_list))
    platform_list = sorted(remove_duplicates_by_list(platform_list))
    session.close()
    return types_list, platform_list


def search_vulnerabilities_advanced(searched_text, db_table, operator_filter, type_filter, platform_filter, author_filter,
                                    port_filter, date_from_filter, date_to_filter):
    """
    Perform a search based on filter selected by the user for an input search.
    :param searched_text: the search input.
    :param db_table: the DB table in which we want to perform the search.
    :param operator_filter: OR operator matches all search results that contain at least one search keyword,
                            AND operator matches only search results that contain all the search keywords.
    :param type_filter: the filter on the vulnerabilities' type.
    :param platform_filter: the filter on the vulnerabilities' platform.
    :param author_filter: the filter on the vulnerabilities' author.
    :param port_filter: the filter on the exploits' port.
    :param date_from_filter: the filter on the vulnerabilities' date (from).
    :param date_to_filter: the filter on the vulnerabilities' date (to).
    :return: a queryset containing all the search results.
    """
    session = start_session()
    words_list = str(searched_text).upper().split()
    if operator_filter == 'AND' and searched_text != '':
        vulnerabilities_list = search_vulnerabilities_for_description_advanced(searched_text, db_table)
    elif operator_filter == 'OR':
        if db_table == 'searcher_exploit':
            queryset = session.query(Exploit).filter(or_(Exploit.description.contains(word) for word in words_list))
        else:
            queryset = session.query(Shellcode).filter(or_(Shellcode.description.contains(word) for word in words_list))
        vulnerabilities_list = queryset2list(queryset)
    else:
        if db_table == 'searcher_exploit':
            queryset = session.query(Exploit)
        else:
            queryset = session.query(Shellcode)
        vulnerabilities_list = queryset2list(queryset)
    if type_filter != 'all':
        vulnerabilities_list = filter_vulnerabilities_for_type(vulnerabilities_list, type_filter)
    if platform_filter != 'all':
        vulnerabilities_list = filter_vulnerabilities_for_platform(vulnerabilities_list, platform_filter)
    if author_filter != '':
        vulnerabilities_list = filter_vulnerabilities_for_author(vulnerabilities_list, author_filter)
    try:
        date_from = datetime.datetime.strptime(date_from_filter, '%Y-%m-%d')
        date_to = datetime.datetime.strptime(date_to_filter, '%Y-%m-%d')
        vulnerabilities_list = filter_vulnerabilities_for_date_range(vulnerabilities_list, date_from, date_to)
    except ValueError:
        pass
    if port_filter != '' and db_table == 'searcher_exploit':
        vulnerabilities_list = filter_exploits_for_port(vulnerabilities_list, port_filter)
    elif port_filter != '' and db_table == 'searcher_shellcode':
        vulnerabilities_list = []

    queryset_std = search_vulnerabilities_for_text_input_advanced(searched_text, db_table, type_filter, platform_filter,
                                                                  author_filter, port_filter, date_from_filter,
                                                                  date_to_filter)
    results_list = join_lists(vulnerabilities_list, queryset_std)
    session.close()
    return results_list


def search_vulnerabilities_for_description_advanced(searched_text, db_table):
    """
    If the search input contains a number of version, it calls 'search_vulnerabilities_version' method,
    else it calls 'search_vulnerabilities_for_description'.
    :param searched_text: the search input.
    :param db_table: the DB table in which we want to perform the search.
    :return: a queryset containing all the search results that can be filtered with the filters selected by the user.
    """
    words_list = str(searched_text).upper().split()
    if str_is_num_version(str(searched_text)) and str(searched_text).__contains__(' ') \
            and not str(searched_text).__contains__('<'):
        queryset = search_vulnerabilities_version(words_list, db_table)
    else:
        queryset = search_vulnerabilities_for_description(words_list, db_table)
    return queryset


def search_vulnerabilities_for_text_input_advanced(searched_text, db_table, type_filter, platform_filter, author_filter,
                                                   port_filter, date_from_filter, date_to_filter):
    """
    Perform a search based on characters contained by this attribute.
    :param searched_text: the search input.
    :param db_table: the DB table in which we want to perform the search.
    :param type_filter: the filter on the vulnerabilities' type.
    :param platform_filter: the filter on the vulnerabilities' platform.
    :param author_filter: the filter on the vulnerabilities' author.
    :param port_filter: the filter on the exploits' port.
    :param date_from_filter: the filter on the vulnerabilities' date (from).
    :param date_to_filter: the filter on the vulnerabilities' date (to).
    :return: a queryset containing all the search results.
    """
    vulnerabilities_list = search_vulnerabilities_for_text_input(searched_text, db_table)
    if type_filter != 'all':
        vulnerabilities_list = filter_vulnerabilities_for_type(vulnerabilities_list, type_filter)
    if platform_filter != 'all':
        vulnerabilities_list = filter_vulnerabilities_for_platform(vulnerabilities_list, platform_filter)
    if author_filter != '':
        vulnerabilities_list = filter_vulnerabilities_for_author(vulnerabilities_list, author_filter)
    try:
        date_from = datetime.datetime.strptime(date_from_filter, '%Y-%m-%d')
        date_to = datetime.datetime.strptime(date_to_filter, '%Y-%m-%d')
        vulnerabilities_list = filter_vulnerabilities_for_date_range(vulnerabilities_list, date_from, date_to)
    except ValueError:
        pass
    if port_filter != '' and db_table == 'searcher_exploit':
        vulnerabilities_list = filter_exploits_for_port(vulnerabilities_list, port_filter)
    elif port_filter != '' and db_table == 'searcher_shellcode':
        vulnerabilities_list = []
    return vulnerabilities_list

