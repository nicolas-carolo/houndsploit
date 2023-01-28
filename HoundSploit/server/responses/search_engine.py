from flask import render_template
from HoundSploit.searcher.engine.suggestions import propose_suggestions, substitute_with_suggestions
from HoundSploit.searcher.entities.exploit import Exploit
from HoundSploit.searcher.entities.shellcode import Shellcode
from HoundSploit.searcher.engine.sorter import sort_results
from HoundSploit.searcher.utils.searcher import get_n_needed_pages_for_showing_results
from HoundSploit.searcher.utils.constants import N_RESULTS_FOR_PAGE
from HoundSploit.searcher.engine.keywords_highlighter import highlight_keywords_in_description, highlight_keywords_in_file, \
    highlight_keywords_in_port
from HoundSploit.searcher.utils.searcher import get_index_first_result, get_index_last_result, get_n_needed_pages_for_showing_results



def render_home_page():
    return render_template('home.html', current_exploits_page=1, current_shellcodes_page=1, sorting_type="Most recent")


def render_search_results(searched_text, search_params):
    current_exploits_page = search_params['current_exploits_page']
    current_shellcodes_page = search_params['current_shellcodes_page']
    current_view = search_params['current_view']
    sorting_type = search_params['sorting_type']
    searched_text = substitute_with_suggestions(searched_text)
    suggested_search_text = propose_suggestions(searched_text)
    key_words_list = (str(searched_text).upper()).split()
    exploits_list, n_exploits, last_exploits_page = get_exploit_results(searched_text, sorting_type, current_exploits_page)
    shellcodes_list, n_shellcodes, last_shellcodes_page = get_shellcode_results(searched_text, sorting_type, current_shellcodes_page)
    exploits_list, shellcodes_list = highlight_keywords_if_searched_text_is_numeric(searched_text, exploits_list, shellcodes_list)
    exploits_list = highlight_keywords_in_description(key_words_list, exploits_list)
    shellcodes_list = highlight_keywords_in_description(key_words_list, shellcodes_list)
    return render_template('results_table.html', searched_item=searched_text,
                        exploits_list=exploits_list, shellcodes_list=shellcodes_list,
                        searched_text=searched_text, suggested_search_text=suggested_search_text,
                        n_exploits=n_exploits, current_exploits_page=current_exploits_page,
                        last_exploits_page=last_exploits_page, current_view=current_view,
                        n_shellcodes=n_shellcodes, current_shellcodes_page=current_shellcodes_page,
                        last_shellcodes_page=last_shellcodes_page, sorting_type=sorting_type)


def get_exploit_results(searched_text, sorting_type, current_exploits_page):
    exploits_list = Exploit.search(searched_text)
    exploits_list = sort_results(exploits_list, sorting_type)
    n_exploits = len(exploits_list)
    last_exploits_page = get_n_needed_pages_for_showing_results(n_exploits)
    if current_exploits_page > last_exploits_page:
        current_exploits_page = last_exploits_page
    index_first_result = get_index_first_result(current_exploits_page)
    index_last_result = get_index_last_result(index_first_result)
    exploits_list = exploits_list[index_first_result:index_last_result]
    exploits_list = normalize_exploit_results(exploits_list)
    return exploits_list, n_exploits, last_exploits_page


def get_shellcode_results(searched_text, sorting_type, current_shellcodes_page):
    shellcodes_list = Shellcode.search(searched_text)
    shellcodes_list = sort_results(shellcodes_list, sorting_type)
    n_shellcodes = len(shellcodes_list)
    last_shellcodes_page = get_n_needed_pages_for_showing_results(n_shellcodes)
    if current_shellcodes_page > last_shellcodes_page:
        current_shellcodes_page = last_shellcodes_page
    index_first_result = get_index_first_result(current_shellcodes_page)
    index_last_result = get_index_last_result(index_first_result)
    shellcodes_list = shellcodes_list[index_first_result:index_last_result]
    return shellcodes_list, n_shellcodes, last_shellcodes_page


def highlight_keywords_if_searched_text_is_numeric(searched_text, exploits_list, shellcodes_list):
    if str(searched_text).isnumeric():
        exploits_list = highlight_keywords_in_file(key_words_list, exploits_list)
        shellcodes_list = highlight_keywords_in_file(key_words_list, shellcodes_list)
        exploits_list = highlight_keywords_in_port(key_words_list, exploits_list)
    return exploits_list, shellcodes_list


def normalize_exploit_results(exploits_list):
    for result in exploits_list:
        if result.port is None:
            result.port = ''
    return exploits_list