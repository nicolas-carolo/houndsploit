import os
import shutil
import sys
import datetime
import platform

from flask import Flask, render_template, request
from HoundSploit.searcher.utils.searcher import get_vulnerability_filters
from HoundSploit.searcher.engine.keywords_highlighter import highlight_keywords_in_description, highlight_keywords_in_file, \
    highlight_keywords_in_port
from HoundSploit.searcher.engine.suggestions import substitute_with_suggestions, propose_suggestions, get_suggestions_list,\
    new_suggestion, remove_suggestion
from HoundSploit.searcher.utils.searcher import get_n_needed_pages_for_showing_results
from HoundSploit.searcher.engine.csv2sqlite import create_db
from HoundSploit.searcher.engine.sorter import sort_results
from shutil import copyfile
from HoundSploit.searcher.entities.exploit import Exploit
from HoundSploit.searcher.entities.shellcode import Shellcode
from HoundSploit.searcher.utils.file import check_file_existence, download_vulnerability_file
from HoundSploit.searcher.utils.constants import BASE_DIR, TEMPLATE_DIR, STATIC_DIR, N_RESULTS_FOR_PAGE, DEFAULT_SUGGESTIONS

from HoundSploit.server.requests.details import get_exploit_from_params, get_shellcode_from_params
from HoundSploit.server.requests.search_engine import get_searched_text, is_previous_page_bookmarks
from HoundSploit.server.requests.suggestions import get_searched_text_suggestion, get_search_suggestion, get_suggestion_autoreplacement_flag
from HoundSploit.server.responses.details import render_vulnerability_details
from HoundSploit.server.responses.error_page import render_error_page
from HoundSploit.server.responses.settings import render_settings
from HoundSploit.server.responses.suggestions import render_suggestions
from HoundSploit.searcher.engine.updates import install_updates, check_db_changes,check_software_changes, check_no_updates
from HoundSploit.searcher.engine.bookmarks import new_bookmark, is_bookmarked, remove_bookmark, get_bookmarks_list
from HoundSploit.searcher.engine.suggestions import new_suggestion

def request_search_results():
    if request.method == 'POST':
        current_exploits_page = request.form['hid-e-page']
        current_view = request.form['current-view']
        try:
            current_exploits_page = int(current_exploits_page)
        except ValueError:
            current_exploits_page = 1

        current_shellcodes_page = request.form['hid-s-page']
        current_view = request.form['current-view']
        try:
            current_shellcodes_page = int(current_shellcodes_page)
        except ValueError:
            current_shellcodes_page = 1

        sorting_type = request.form['sorting-type']

        searched_text = request.form['searched-text']
        searched_text = substitute_with_suggestions(searched_text)
        suggested_search_text = propose_suggestions(searched_text)
        if str(searched_text).isspace() or searched_text == "":
            return render_template('home.html', current_exploits_page=1, current_shellcodes_page=1, sorting_type="Most recent")
        key_words_list = (str(searched_text).upper()).split()
        
        exploits_list = Exploit.search(searched_text)
        exploits_list = sort_results(exploits_list, sorting_type)
        n_exploits = len(exploits_list)

        latest_exploits_page = get_n_needed_pages_for_showing_results(n_exploits)
        if current_exploits_page < 1:
            current_exploits_page = 1
            index_first_result = 0
        elif current_exploits_page > latest_exploits_page:
            current_exploits_page = latest_exploits_page
            index_first_result = (int(current_exploits_page) - 1) * N_RESULTS_FOR_PAGE
        else:
            index_first_result = (int(current_exploits_page) - 1) * N_RESULTS_FOR_PAGE
        index_last_result = index_first_result + N_RESULTS_FOR_PAGE
        exploits_list = exploits_list[index_first_result:index_last_result]
        for result in exploits_list:
            if result.port is None:
                result.port = ''


        shellcodes_list = Shellcode.search(searched_text)
        shellcodes_list = sort_results(shellcodes_list, sorting_type)
        n_shellcodes = len(shellcodes_list)

        latest_shellcodes_page = get_n_needed_pages_for_showing_results(n_shellcodes)
        if current_shellcodes_page < 1:
            current_shellcodes_page = 1
            index_first_result = 0
        elif current_shellcodes_page > latest_shellcodes_page:
            current_shellcodes_page = latest_shellcodes_page
            index_first_result = (int(current_shellcodes_page) - 1) * N_RESULTS_FOR_PAGE
        else:
            index_first_result = (int(current_shellcodes_page) - 1) * N_RESULTS_FOR_PAGE
        index_last_result = index_first_result + N_RESULTS_FOR_PAGE
        shellcodes_list = shellcodes_list[index_first_result:index_last_result]

        if str(searched_text).isnumeric():
            exploits_list = highlight_keywords_in_file(key_words_list, exploits_list)
            shellcodes_list = highlight_keywords_in_file(key_words_list, shellcodes_list)
            exploits_list = highlight_keywords_in_port(key_words_list, exploits_list)
        exploits_list = highlight_keywords_in_description(key_words_list, exploits_list)
        shellcodes_list = highlight_keywords_in_description(key_words_list, shellcodes_list)
        return render_template('results_table.html', searched_item=searched_text,
                               exploits_list=exploits_list, shellcodes_list=shellcodes_list,
                               searched_text=searched_text, suggested_search_text=suggested_search_text,
                               n_exploits=n_exploits, current_exploits_page=current_exploits_page,
                               latest_exploits_page=latest_exploits_page, current_view=current_view,
                               n_shellcodes=n_shellcodes, current_shellcodes_page=current_shellcodes_page,
                               latest_shellcodes_page=latest_shellcodes_page, sorting_type=sorting_type)
    else:
        return render_template('home.html', current_exploits_page=1, current_shellcodes_page=1, sorting_type="Most recent")


def request_advanced_search_results():
    vulnerability_types_list, vulnerability_platforms_list = get_vulnerability_filters()
    if request.method == 'POST':
        current_exploits_page = request.form['hid-e-page']
        current_view = request.form['current-view']
        try:
            current_exploits_page = int(current_exploits_page)
        except ValueError:
            current_exploits_page = 1

        current_shellcodes_page = request.form['hid-s-page']
        current_view = request.form['current-view']
        try:
            current_shellcodes_page = int(current_shellcodes_page)
        except ValueError:
            current_shellcodes_page = 1

        sorting_type = request.form['sorting-type']

        searched_text = request.form['searched-text']
        # TODO fix suggestions bug
        #searched_text = substitute_with_suggestions(searched_text),
        #suggested_search_text = propose_suggestions(searched_text)
        suggested_search_text = ""

        filters = {
            "operator": request.form['search-operator'],
            "author": request.form['author'],
            "type": request.form['type'],
            "platform": request.form['platform'],
            "port": request.form['port'],
            "date_from": request.form['date-from'],
            "date_to": request.form['date-to'],
        }
        
        
        if str(searched_text).isspace() or searched_text == "":
            return render_template('advanced_searcher.html',
                                vulnerability_types_list=vulnerability_types_list,
                                vulnerability_platforms_list=vulnerability_platforms_list,
                                current_exploits_page=1,
                                current_shellcodes_page=1, sorting_type="Most recent")
        key_words_list = (str(searched_text).upper()).split()

        date_alert = None
        try:
            date_from = datetime.datetime.strptime(filters["date_from"], '%Y-%m-%d')
            date_to = datetime.datetime.strptime(filters["date_to"], '%Y-%m-%d')
            if date_from > date_to:
                filters["date_from"] = "mm/dd/yyyy"
                filters["date_to"] = "mm/dd/yyyy"
                date_alert = "ERROR: date range not valid!"
        except ValueError:
            filters["date_from"] = "mm/dd/yyyy"
            filters["date_to"] = "mm/dd/yyyy"

        exploits_list = Exploit.advanced_search(searched_text, filters)
        exploits_list = sort_results(exploits_list, sorting_type)
        n_exploits = len(exploits_list)

        latest_exploits_page = get_n_needed_pages_for_showing_results(n_exploits)
        if current_exploits_page < 1:
            current_exploits_page = 1
            index_first_result = 0
        elif current_exploits_page > latest_exploits_page:
            current_exploits_page = latest_exploits_page
            index_first_result = (int(current_exploits_page) - 1) * N_RESULTS_FOR_PAGE
        else:
            index_first_result = (int(current_exploits_page) - 1) * N_RESULTS_FOR_PAGE
        index_last_result = index_first_result + N_RESULTS_FOR_PAGE
        exploits_list = exploits_list[index_first_result:index_last_result]

        for result in exploits_list:
            if result.port is None:
                result.port = ''
        
        shellcodes_list = Shellcode.advanced_search(searched_text, filters)
        shellcodes_list = sort_results(shellcodes_list, sorting_type)
        n_shellcodes = len(shellcodes_list)

        latest_shellcodes_page = get_n_needed_pages_for_showing_results(n_shellcodes)
        if current_shellcodes_page < 1:
            current_shellcodes_page = 1
            index_first_result = 0
        elif current_shellcodes_page > latest_shellcodes_page:
            current_shellcodes_page = latest_shellcodes_page
            index_first_result = (int(current_shellcodes_page) - 1) * N_RESULTS_FOR_PAGE
        else:
            index_first_result = (int(current_shellcodes_page) - 1) * N_RESULTS_FOR_PAGE
        index_last_result = index_first_result + N_RESULTS_FOR_PAGE
        shellcodes_list = shellcodes_list[index_first_result:index_last_result]

        if str(searched_text).isnumeric():
            exploits_list = highlight_keywords_in_file(key_words_list, exploits_list)
            shellcodes_list = highlight_keywords_in_file(key_words_list, shellcodes_list)
            exploits_list = highlight_keywords_in_port(key_words_list, exploits_list)
        exploits_list = highlight_keywords_in_description(key_words_list, exploits_list)
        shellcodes_list = highlight_keywords_in_description(key_words_list, shellcodes_list)
        return render_template('advanced_results_table.html',
                            searched_item=searched_text,
                            exploits_list=exploits_list,
                            shellcodes_list=shellcodes_list,
                            searched_text=searched_text,
                            vulnerability_types_list=vulnerability_types_list,
                            vulnerability_platforms_list=vulnerability_platforms_list,
                            operator_filter=filters["operator"],
                            author_filter=filters["author"],
                            type_filter=filters["type"],
                            platform_filter=filters["platform"],
                            port_filter=filters["port"],
                            date_from_filter=filters["date_from"],
                            date_to_filter=filters["date_to"],
                            suggested_search_text=suggested_search_text,
                            date_alert=date_alert,
                            n_exploits=n_exploits,
                            current_exploits_page=current_exploits_page,
                            latest_exploits_page=latest_exploits_page,
                            current_view=current_view,
                            n_shellcodes=n_shellcodes,
                            current_shellcodes_page=current_shellcodes_page,
                            latest_shellcodes_page=latest_shellcodes_page,
                            sorting_type=sorting_type
                            )
    else:
        return render_template('advanced_searcher.html',
                            vulnerability_types_list=vulnerability_types_list,
                            vulnerability_platforms_list=vulnerability_platforms_list,
                            current_exploits_page=1,
                            current_shellcodes_page=1,
                            sorting_type="Most recent"
                            )


def request_exploit_details():
    exploit = get_exploit_from_params(request)
    searched_text = get_searched_text(request)
    is_prev_page_bookmarks = is_previous_page_bookmarks(request)
    return render_vulnerability_details(exploit, is_prev_page_bookmarks, None)  


def request_shellcode_details():
    shellcode = get_shellcode_from_params(request)
    searched_text = get_searched_text(request)
    is_prev_page_bookmarks = is_previous_page_bookmarks(request)
    return render_vulnerability_details(shellcode, is_prev_page_bookmarks, None) 


def request_download_exploit():
    exploit = get_exploit_from_params(request)
    status, message = download_vulnerability_file(exploit)
    is_prev_page_bookmarks = is_previous_page_bookmarks(request)
    if status:
        return render_vulnerability_details(exploit, is_prev_page_bookmarks, message)
    else:
        return render_error_page(message)


def request_download_shellcode():
    shellcode = get_shellcode_from_params(request)
    print(shellcode.id)
    status, message = download_vulnerability_file(shellcode)
    is_prev_page_bookmarks = is_previous_page_bookmarks(request)
    if status:
        return render_vulnerability_details(shellcode, is_prev_page_bookmarks, message)
    else:
        return render_error_page(message)


def request_add_bookmark_exploit():
    exploit = get_exploit_from_params(request)
    is_prev_page_bookmarks = is_previous_page_bookmarks(request)
    status, message = new_bookmark(exploit)
    if status:
        return render_vulnerability_details(exploit, is_prev_page_bookmarks, None)
    else:
        return render_error_page(message)


def request_add_bookmark_shellcode():
    shellcode = get_shellcode_from_params(request)
    is_prev_page_bookmarks = is_previous_page_bookmarks(request)
    status, message = new_bookmark(shellcode)
    if status:
        return render_vulnerability_details(shellcode, is_prev_page_bookmarks, None)
    else:
        return render_error_page(message)


def request_delete_bookmark_exploit():
    exploit = get_exploit_from_params(request)
    is_prev_page_bookmarks = is_previous_page_bookmarks(request)
    status, message = remove_bookmark(exploit)
    if status:
        return render_vulnerability_details(exploit, is_prev_page_bookmarks, None)
    else:
        return render_error_page(message)


def request_delete_bookmark_shellcode():
    shellcode = get_shellcode_from_params(request)
    is_prev_page_bookmarks = is_previous_page_bookmarks(request)
    status, message = remove_bookmark(shellcode)
    if status:
        return render_vulnerability_details(shellcode, is_prev_page_bookmarks, None)
    else:
        return render_error_page(message)



def request_settings():
    return render_settings(False, False, False)


def request_update():
    install_updates()
    db_update_alert = check_db_changes()
    sw_update_alert = check_software_changes()
    no_updates_alert = check_no_updates(db_update_alert, sw_update_alert)
    return render_settings(db_update_alert, sw_update_alert, no_updates_alert)
    

def request_suggestions_manager():
    return render_template('suggestions.html', suggestions=get_suggestions_list(), default_suggestions=DEFAULT_SUGGESTIONS)


def request_add_suggestion():
    searched = get_searched_text_suggestion(request)
    suggestion = get_search_suggestion(request)
    autoreplacement = get_suggestion_autoreplacement_flag(request)
    status, message = new_suggestion(searched, suggestion, autoreplacement)
    if (status):
        return render_suggestions()
    else:
        return render_error_page(message)


def request_delete_suggestion():
    searched = get_searched_text_suggestion(request)
    status, message = remove_suggestion(searched)
    if (status):
        return render_suggestions()
    else:
        return render_error_page(message)


def request_bookmarks_manager():
    searched_text = ""
    bookmarks_list = get_bookmarks_list()
    key_words_list = []

    if request.method == 'POST':
        searched_text = request.form['searched-text']
        current_bookmarks_page = int(request.form['hid-b-page'])
    else:
        current_bookmarks_page = 1
        searched_text = request.args.get('searched', None)
    
    if searched_text is None:
        searched_text = ""
    

    if searched_text != "":
        key_words_list = (str(searched_text).upper()).split()
        exploits_list = Exploit.search(searched_text)
        shellcodes_list = Shellcode.search(searched_text)
        results_list = exploits_list + shellcodes_list
        filtered_bookmarks_list = []
        for result in results_list:
            for bookmark in bookmarks_list:
                if result.description == bookmark.description:
                    filtered_bookmarks_list.append(bookmark)
        bookmarks_list = filtered_bookmarks_list


    n_bookmarks = len(bookmarks_list)
    latest_bookmarks_page = get_n_needed_pages_for_showing_results(n_bookmarks)

    if current_bookmarks_page < 1:
        current_bookmarks_page = 1
        index_first_result = 0
    elif current_bookmarks_page > latest_bookmarks_page:
        current_bookmarks_page = latest_bookmarks_page
        index_first_result = (int(current_bookmarks_page) - 1) * N_RESULTS_FOR_PAGE
    else:
        index_first_result = (int(current_bookmarks_page) - 1) * N_RESULTS_FOR_PAGE
    index_last_result = index_first_result + N_RESULTS_FOR_PAGE
    bookmarks_list = bookmarks_list[index_first_result:index_last_result]
    bookmarks_list = highlight_keywords_in_description(key_words_list, bookmarks_list)

    return render_template('bookmarks.html', searched_text=searched_text,
                            bookmarks_list=bookmarks_list,
                            current_bookmarks_page=current_bookmarks_page,
                            latest_bookmarks_page=latest_bookmarks_page)