import os
import shutil
import sys
import datetime
import platform

from flask import Flask, render_template, request
from HoundSploit.searcher.engine.search_engine import get_vulnerability_filters
from HoundSploit.searcher.engine.keywords_highlighter import highlight_keywords_in_description, highlight_keywords_in_file, \
    highlight_keywords_in_port
from HoundSploit.searcher.engine.suggestions import substitute_with_suggestions, propose_suggestions, get_suggestions_list,\
    new_suggestion, remove_suggestion, DEFAULT_SUGGESTIONS
from HoundSploit.searcher.engine.updates import get_latest_db_update_date, install_updates
from HoundSploit.searcher.utils.searcher import get_n_needed_pages_for_showing_results
from HoundSploit.searcher.engine.csv2sqlite import create_db
from HoundSploit.searcher.engine.sorter import sort_results
from HoundSploit.searcher.engine.bookmarks import new_bookmark, is_bookmarked, remove_bookmark, get_bookmarks_list
from HoundSploit.searcher.engine.fix_dates import fix_dates, create_fixed_db
from shutil import copyfile
from HoundSploit.searcher.entities.exploit import Exploit
from HoundSploit.searcher.entities.shellcode import Shellcode
from HoundSploit.searcher.utils.file import check_file_existence


init_path = os.path.abspath(os.path.expanduser("~") + "/.HoundSploit")
template_dir = os.path.abspath(init_path + '/houndsploit/HoundSploit/templates')
static_folder = os.path.abspath(init_path + '/houndsploit/HoundSploit/static')


app = Flask(__name__, template_folder=template_dir, static_folder=static_folder)

N_RESULTS_FOR_PAGE = 10


@app.route('/', methods=['GET', 'POST'])
def get_results_table():
    """
    Render a table with a list of search results.
    :return: results_table.html template with search results.
    """
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


@app.route('/advanced-search', methods=['GET', 'POST'])
def get_results_table_advanced():
    """
    Render a table with a list of search results.
    :return: results_table.html template with search results.
    """
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


@app.route('/exploit-details')
def view_exploit_details():
    """
    Open details about the selected exploit, included the source code.
    :return: a template showing the details about the selected exploit and the source code.
    """
    vulnerability_class = "exploit"
    exploit_id = request.args.get('exploit-id', None)
    searched_text = request.args.get('searched-text', None)
    is_prev_page_bookmarks = request.args.get('isprevpagebookmarks', None)
    if is_prev_page_bookmarks == "true":
        is_prev_page_bookmarks = True
    else:
        is_prev_page_bookmarks = False
    exploit = Exploit.get_by_id(exploit_id)
    if exploit is None:
        error_msg = 'Sorry! This exploit does not exist :('
        return render_template('error_page.html', error=error_msg)
    file_path = init_path + "/exploitdb/" + exploit.file
    try:
        with open(file_path, 'r') as f:
            content = f.readlines()
            vulnerability_code = ''.join(content)
        return render_template('code_viewer.html', vulnerability_code=vulnerability_code,
                               vulnerability_description=exploit.description, vulnerability_file=exploit.file,
                               vulnerability_author=exploit.author, vulnerability_date=exploit.date,
                               vulnerability_type=exploit.type, vulnerability_platform=exploit.platform,
                               vulnerability_port=exploit.port, file_path=file_path, exploit_id=exploit_id,
                               bookmarked=is_bookmarked(exploit_id, vulnerability_class),
                               searched_text=searched_text, is_prev_page_bookmarks=is_prev_page_bookmarks)
    except FileNotFoundError:
        error_msg = 'Sorry! This file does not exist :('
        return render_template('error_page.html', error=error_msg)


@app.route('/download-exploit')
def download_exploit_details():
    """
    Download the selected exploit.
    :return: a template showing the details about the selected exploit and the source code.
    """
    vulnerability_class = "exploit"
    exploit_id = request.args.get('exploit-id', None)
    exploit = Exploit.get_by_id(exploit_id)
    if exploit is None:
        error_msg = 'Sorry! This exploit does not exist :('
        return render_template('error_page.html', error=error_msg)
    file_path = init_path + "/exploitdb/" + exploit.file
    try:
        with open(file_path, 'r') as f:
            content = f.readlines()
            vulnerability_code = ''.join(content)
        copyfile(file_path, os.path.expanduser("~") + "/exploit_" + exploit_id + exploit.get_extension())
        download_alert = "exploit_" + exploit_id + exploit.get_extension() + " has been downloaded in your home directory"
        return render_template('code_viewer.html', vulnerability_code=vulnerability_code,
                               vulnerability_description=exploit.description, vulnerability_file=exploit.file,
                               vulnerability_author=exploit.author, vulnerability_date=exploit.date,
                               vulnerability_type=exploit.type, vulnerability_platform=exploit.platform,
                               vulnerability_port=exploit.port, file_path=file_path, download_alert=download_alert,
                               exploit_id=exploit_id, bookmarked=is_bookmarked(exploit_id, vulnerability_class))
    except FileNotFoundError:
        error_msg = 'Sorry! This file does not exist :('
        return render_template('error_page.html', error=error_msg)


@app.route('/shellcode-details')
def view_shellcode_details():
    """
    Open details about the selected shellcode, included the source code.
    :return: a template showing the details about the selected shellcode and the source code.
    """
    vulnerability_class = "shellcode"
    shellcode_id = request.args.get('shellcode-id', None)
    searched_text = request.args.get('searched-text', None)
    is_prev_page_bookmarks = request.args.get('isprevpagebookmarks', None)
    if is_prev_page_bookmarks == "true":
        is_prev_page_bookmarks = True
    else:
        is_prev_page_bookmarks = False
    shellcode = Shellcode.get_by_id(shellcode_id)
    if shellcode is None:
        error_msg = 'Sorry! This shellcode does not exist :('
        return render_template('error_page.html', error=error_msg)
    file_path = init_path + "/exploitdb/" + shellcode.file
    try:
        with open(file_path, 'r') as f:
            content = f.readlines()
            vulnerability_code = ''.join(content)
        return render_template('code_viewer.html',
                            vulnerability_code=vulnerability_code,
                            vulnerability_description=shellcode.description,
                            vulnerability_file=shellcode.file,
                            vulnerability_author=shellcode.author,
                            vulnerability_date=shellcode.date,
                            vulnerability_type=shellcode.type,
                            vulnerability_platform=shellcode.platform,
                            file_path=file_path,
                            shellcode_id=shellcode_id,
                            bookmarked=is_bookmarked(shellcode_id, vulnerability_class),
                            searched_text=searched_text,
                            is_prev_page_bookmarks=is_prev_page_bookmarks
                            )
    except FileNotFoundError:
        error_msg = 'Sorry! This file does not exist :('
        return render_template('error_page.html', error=error_msg)


@app.route('/download-shellcode')
def download_shellcode():
    """
    Download the selected shellcode.
    :return: a template showing the details about the selected shellcode and the source code.
    """
    vulnerability_class = "shellcode"
    shellcode_id = request.args.get('shellcode-id', None)
    shellcode = Shellcode.get_by_id(shellcode_id)
    if shellcode is None:
        error_msg = 'Sorry! This shellcode does not exist :('
        return render_template('error_page.html', error=error_msg)
    file_path = init_path + "/exploitdb/" + shellcode.file
    try:
        with open(file_path, 'r') as f:
            content = f.readlines()
            vulnerability_code = ''.join(content)
        copyfile(file_path, os.path.expanduser("~") + "/shellcode_" + shellcode_id + shellcode.get_extension())
        download_alert = "shellcode_" + shellcode_id + shellcode.get_extension() + " has been downloaded in your home directory"
        return render_template('code_viewer.html',
                            vulnerability_code=vulnerability_code,
                            vulnerability_description=shellcode.description,
                            vulnerability_file=shellcode.file,
                            vulnerability_author=shellcode.author,
                            vulnerability_date=shellcode.date,
                            vulnerability_type=shellcode.type,
                            vulnerability_platform=shellcode.platform,
                            file_path=file_path,
                            download_alert=download_alert,
                            shellcode_id=shellcode_id,
                            bookmarked=is_bookmarked(shellcode_id, vulnerability_class)
                            )
    except FileNotFoundError:
        error_msg = 'Sorry! This file does not exist :('
        return render_template('error_page.html', error=error_msg)


@app.route('/settings')
def settings():
    """
    Show settings page
    :return: settings templates
    """
    return render_template('settings.html', latest_db_update=get_latest_db_update_date())


@app.route('/update')
def get_updates():
    """
    Check and download new updates for the software and the database
    :return: settings templates
    """
    install_updates()
    if check_file_existence(init_path + "/houndsploit_db.lock"):
        if os.path.isdir(init_path + "/fixed_exploitdb"):
            create_fixed_db()
        else:
            if check_file_existence(init_path + "/hound_db.sqlite3"):
                os.remove(init_path + "/hound_db.sqlite3")
            create_db()
        db_update_alert = True
    else:
        db_update_alert = False

    if check_file_existence(init_path + "/houndsploit_sw.lock"):
        sw_update_alert = True
    else:
        sw_update_alert = False

    if sw_update_alert == False and db_update_alert == False:
        no_updates_alert = True
    else:
        no_updates_alert = False

    return render_template('settings.html', latest_db_update=get_latest_db_update_date(), db_update_alert=db_update_alert,
                            sw_update_alert=sw_update_alert, no_updates_alert=no_updates_alert)


@app.route('/suggestions')
def suggestions_manager():
    """
    Open suggestions manager
    :return: suggestion manager template
    """
    return render_template('suggestions.html', suggestions=get_suggestions_list(), default_suggestions=DEFAULT_SUGGESTIONS)


@app.route('/add-suggestion', methods=['GET', 'POST'])
def add_suggestion():
    """
    Add a new suggestion inserted by the user.
    :return: the 'suggestions.html' template. In case of error it shows an error message.
    """
    if request.method == 'POST':
        searched = request.form['searched']
        suggestion = request.form['suggestion']
        autoreplacement = request.form['autoreplacement']
        if not str(searched).lower() in DEFAULT_SUGGESTIONS:
            new_suggestion(searched, suggestion, autoreplacement)
            return render_template('suggestions.html', suggestions=get_suggestions_list(), default_suggestions=DEFAULT_SUGGESTIONS)
        else:
            error = 'ERROR: Default suggestions cannot be modified!'
            return render_template('suggestions.html', suggestions=get_suggestions_list(), suggestion_error=error, default_suggestions=DEFAULT_SUGGESTIONS)


@app.route('/delete-suggestion')
def delete_suggestion():
    """
    Delete a suggestion selected by the user.
    :return: the 'suggestions.html' template. In case of error it shows an error message.
    """
    searched = request.args.get('searched', None)
    if str(searched).lower() in DEFAULT_SUGGESTIONS:
        error = 'ERROR: Default suggestions cannot be deleted!'
        return render_template('suggestions.html', suggestions=get_suggestions_list(), suggestion_error=error, default_suggestions=DEFAULT_SUGGESTIONS)
    if remove_suggestion(searched):
        return render_template('suggestions.html', suggestions=get_suggestions_list(), default_suggestions=DEFAULT_SUGGESTIONS)
    else:
        error = 'ERROR: The suggestion you want to delete does not exist!'
        return render_template('suggestions.html', suggestions=get_suggestions_list(), suggestion_error=error, default_suggestions=DEFAULT_SUGGESTIONS)


@app.route('/bookmarks', methods=['GET', 'POST'])
def bookmarks_manager():
    """
    Open bookmarks manager
    :return: bookmarks manager template
    """
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


@app.route('/bookmark-exploit')
def bookmark_exploit():
    """
    Bookmark the selected exploit.
    :return: a template showing the details about the selected exploit and the source code.
    """
    vulnerability_class = "exploit"
    exploit_id = request.args.get('exploit-id', None)
    exploit = Exploit.get_by_id(exploit_id)
    if exploit is None:
        error_msg = 'Sorry! This exploit does not exist :('
        return render_template('error_page.html', error=error_msg)
    file_path = init_path + "/exploitdb/" + exploit.file
    try:
        with open(file_path, 'r') as f:
            content = f.readlines()
            vulnerability_code = ''.join(content)
        if new_bookmark(exploit_id, vulnerability_class):
            return render_template('code_viewer.html', vulnerability_code=vulnerability_code,
                                vulnerability_description=exploit.description, vulnerability_file=exploit.file,
                                vulnerability_author=exploit.author, vulnerability_date=exploit.date,
                                vulnerability_type=exploit.type, vulnerability_platform=exploit.platform,
                                vulnerability_port=exploit.port, file_path=file_path, exploit_id=exploit_id,
                                bookmarked=is_bookmarked(exploit_id, vulnerability_class))
        else:
            error_msg = 'Sorry! This exploit does not exist :('
            return render_template('error_page.html', error=error_msg)
    except FileNotFoundError:
        error_msg = 'Sorry! This file does not exist :('
        return render_template('error_page.html', error=error_msg)


@app.route('/remove-bookmark-exploit')
def remove_bookmark_exploit():
    """
    Remove the bookmark for the selected exploit.
    :return: a template showing the details about the selected exploit and the source code.
    """
    vulnerability_class = "exploit"
    exploit_id = request.args.get('exploit-id', None)
    exploit = Exploit.get_by_id(exploit_id)
    if exploit is None:
        error_msg = 'Sorry! This exploit does not exist :('
        return render_template('error_page.html', error=error_msg)
    file_path = init_path + "/exploitdb/" + exploit.file
    try:
        with open(file_path, 'r') as f:
            content = f.readlines()
            vulnerability_code = ''.join(content)
        test = remove_bookmark(exploit_id, vulnerability_class)
        return render_template('code_viewer.html', vulnerability_code=vulnerability_code,
                               vulnerability_description=exploit.description, vulnerability_file=exploit.file,
                               vulnerability_author=exploit.author, vulnerability_date=exploit.date,
                               vulnerability_type=exploit.type, vulnerability_platform=exploit.platform,
                               vulnerability_port=exploit.port, file_path=file_path, exploit_id=exploit_id,
                               bookmarked=is_bookmarked(exploit_id, vulnerability_class))
    except FileNotFoundError:
        error_msg = 'Sorry! This file does not exist :('
        return render_template('error_page.html', error=error_msg)


@app.route('/bookmark-shellcode')
def bookmark_shellcode():
    """
    Bookmark the selected shellcode.
    :return: a template showing the details about the selected shellcode and the source code.
    """
    vulnerability_class = "shellcode"
    shellcode_id = request.args.get('shellcode-id', None)
    shellcode = Shellcode.get_by_id(shellcode_id)
    if shellcode is None:
        error_msg = 'Sorry! This shellcode does not exist :('
        return render_template('error_page.html', error=error_msg)
    file_path = init_path + "/exploitdb/" + shellcode.file
    try:
        with open(file_path, 'r') as f:
            content = f.readlines()
            vulnerability_code = ''.join(content)
        if new_bookmark(shellcode_id, vulnerability_class):
            return render_template('code_viewer.html', vulnerability_code=vulnerability_code,
                                vulnerability_description=shellcode.description, vulnerability_file=shellcode.file,
                                vulnerability_author=shellcode.author, vulnerability_date=shellcode.date,
                                vulnerability_type=shellcode.type, vulnerability_platform=shellcode.platform,
                                file_path=file_path, shellcode_id=shellcode_id,
                                bookmarked=is_bookmarked(shellcode_id, vulnerability_class))
        else:
            error_msg = 'Sorry! This shellcode does not exist :('
            return render_template('error_page.html', error=error_msg)
    except FileNotFoundError:
        error_msg = 'Sorry! This file does not exist :('
        return render_template('error_page.html', error=error_msg)


@app.route('/remove-bookmark-shellcode')
def remove_bookmark_shellcode():
    """
    Remove the bookmark for the selected shellcode.
    :return: a template showing the details about the selected shellcode and the source code.
    """
    vulnerability_class = "shellcode"
    shellcode_id = request.args.get('shellcode-id', None)
    shellcode = Shellcode.get_by_id(shellcode_id)
    if shellcode is None:
        error_msg = 'Sorry! This shellcode does not exist :('
        return render_template('error_page.html', error=error_msg)
    file_path = init_path + "/exploitdb/" + shellcode.file
    try:
        with open(file_path, 'r') as f:
            content = f.readlines()
            vulnerability_code = ''.join(content)
        remove_bookmark(shellcode_id, vulnerability_class)
        return render_template('code_viewer.html', vulnerability_code=vulnerability_code,
                               vulnerability_description=shellcode.description, vulnerability_file=shellcode.file,
                               vulnerability_author=shellcode.author, vulnerability_date=shellcode.date,
                               vulnerability_type=shellcode.type, vulnerability_platform=shellcode.platform,
                               file_path=file_path, shellcode_id=shellcode_id,
                               bookmarked=is_bookmarked(shellcode_id, vulnerability_class))
    except FileNotFoundError:
        error_msg = 'Sorry! This file does not exist :('
        return render_template('error_page.html', error=error_msg)


@app.route('/fix-dates')
def repair_dates():
    # print("Starting fix")
    fix_dates()
    # print("Ending fix")
    return render_template('settings.html', latest_db_update=get_latest_db_update_date(), db_update_alert=False,
                            sw_update_alert=False, no_updates_alert=False)


@app.route('/restore-exploitdb')
def restore_exploitdb():
    # print("Starting fix")
    if platform.system() == "Windows":
        script_path = os.path.abspath(init_path + "/houndsploit/HoundSploit/scripts/restore_exploitdb.ps1")
        os.system("powershell.exe -ExecutionPolicy Bypass -File " + script_path)
        # print("Ending fix")
        return render_template('error_page.html', error="Please restart the application server for applying changes!")
    else:
        fixed_exploitdb_path = os.path.abspath(init_path + "/fixed_exploitdb")
        db_path = os.path.abspath(init_path + "/hound_db.sqlite3")
        shutil.rmtree(fixed_exploitdb_path)
        os.remove(db_path)
        create_db()
        # print("Ending fix")
        return render_template('settings.html', latest_db_update=get_latest_db_update_date(), db_update_alert=False,
                                sw_update_alert=False, no_updates_alert=False)


def start_app():
    # app.run(debug=True, host='0.0.0.0')
    app.run(debug=False)
