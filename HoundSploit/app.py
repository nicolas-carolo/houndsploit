import os
import sys
import datetime

from flask import Flask, render_template, request
from HoundSploit.searcher.engine.search_engine import search_vulnerabilities_in_db, get_exploit_by_id, get_shellcode_by_id,\
    get_vulnerability_extension, get_vulnerability_filters, search_vulnerabilities_advanced
from HoundSploit.searcher.engine.keywords_highlighter import highlight_keywords_in_description, highlight_keywords_in_file, \
    highlight_keywords_in_port
from HoundSploit.searcher.engine.suggestions import substitute_with_suggestions, propose_suggestions, get_suggestions_list,\
    new_suggestion, remove_suggestion, DEFAULT_SUGGESTIONS
from HoundSploit.searcher.engine.updates import get_latest_db_update_date, install_updates
from HoundSploit.searcher.engine.utils import check_file_existence, get_vulnerability_extension, get_n_needed_pages
from HoundSploit.searcher.engine.csv2sqlite import create_db
from shutil import copyfile


init_path = os.path.expanduser("~") + "/HoundSploit"
# template_dir = os.path.abspath(init_path + '/houndsploit/HoundSploit/templates')
# static_folder = os.path.abspath(init_path + '/houndsploit/HoundSploit/static')
template_dir = os.path.abspath('/home/nicolas/Projects/Python/houndsploit/HoundSploit/templates')
static_folder = os.path.abspath('/home/nicolas/Projects/Python/houndsploit/HoundSploit/static')
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

        searched_text = request.form['searched-text']
        searched_text = substitute_with_suggestions(searched_text)
        suggested_search_text = propose_suggestions(searched_text)
        if str(searched_text).isspace() or searched_text == "":
            return render_template('home.html', current_exploits_page=1)
        key_words_list = (str(searched_text).upper()).split()
        exploits_list = search_vulnerabilities_in_db(searched_text, 'searcher_exploit')
        n_exploits = len(exploits_list)

        latest_exploits_page = get_n_needed_pages(n_exploits)
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
        shellcodes_list = search_vulnerabilities_in_db(searched_text, 'searcher_shellcode')
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
                               latest_exploits_page=latest_exploits_page, current_view=current_view)
    else:
        return render_template('home.html', current_exploits_page=1)


@app.route('/advanced-search', methods=['GET', 'POST'])
def get_results_table_advanced():
    """
    Render a table with a list of search results.
    :return: results_table.html template with search results.
    """
    vulnerability_types_list, vulnerability_platforms_list = get_vulnerability_filters()
    if request.method == 'POST':
        searched_text = request.form['searched-text']
        operator_filter = request.form['search-operator']
        author_filter = request.form['author']
        type_filter = request.form['type']
        platform_filter = request.form['platform']
        port_filter = request.form['port']
        date_from_filter = request.form['date-from']
        date_to_filter = request.form['date-to']
        searched_text = substitute_with_suggestions(searched_text)
        suggested_search_text = propose_suggestions(searched_text)
        if str(searched_text).isspace() or searched_text == "":
            return render_template('advanced_searcher.html', vulnerability_types_list=vulnerability_types_list,
                                   vulnerability_platforms_list=vulnerability_platforms_list)
        key_words_list = (str(searched_text).upper()).split()

        date_alert = None
        try:
            date_from = datetime.datetime.strptime(date_from_filter, '%Y-%m-%d')
            date_to = datetime.datetime.strptime(date_to_filter, '%Y-%m-%d')
            if date_from > date_to:
                date_from_filter = "mm/dd/yyyy"
                date_to_filter = "mm/dd/yyyy"
                date_alert = "ERROR: date range not valid!"
        except ValueError:
            date_from_filter = "mm/dd/yyyy"
            date_to_filter = "mm/dd/yyyy"

        exploits_list = search_vulnerabilities_advanced(searched_text, 'searcher_exploit', operator_filter, type_filter,
                                                        platform_filter, author_filter, port_filter, date_from_filter,
                                                        date_to_filter)
        for result in exploits_list:
            if result.port is None:
                result.port = ''
        shellcodes_list = search_vulnerabilities_advanced(searched_text, 'searcher_shellcode', operator_filter,
                                                          type_filter, platform_filter, author_filter, port_filter,
                                                          date_from_filter, date_to_filter)
        if str(searched_text).isnumeric():
            exploits_list = highlight_keywords_in_file(key_words_list, exploits_list)
            shellcodes_list = highlight_keywords_in_file(key_words_list, shellcodes_list)
            exploits_list = highlight_keywords_in_port(key_words_list, exploits_list)
        exploits_list = highlight_keywords_in_description(key_words_list, exploits_list)
        shellcodes_list = highlight_keywords_in_description(key_words_list, shellcodes_list)
        return render_template('advanced_results_table.html', searched_item=searched_text,
                               exploits_list=exploits_list, shellcodes_list=shellcodes_list,
                               searched_text=searched_text, vulnerability_types_list=vulnerability_types_list,
                               vulnerability_platforms_list=vulnerability_platforms_list, operator_filter=operator_filter,
                               author_filter=author_filter, type_filter=type_filter,
                               platform_filter=platform_filter, port_filter=port_filter,
                               date_from_filter=date_from_filter, date_to_filter=date_to_filter,
                               suggested_search_text=suggested_search_text, date_alert=date_alert)
    else:
        return render_template('advanced_searcher.html', vulnerability_types_list=vulnerability_types_list,
                               vulnerability_platforms_list=vulnerability_platforms_list)


@app.route('/exploit-details')
def view_exploit_details():
    """
    Open details about the selected exploit, included the source code.
    :return: a template showing the details about the selected exploit and the source code.
    """
    exploit_id = request.args.get('exploit-id', None)
    exploit = get_exploit_by_id(exploit_id)
    file_path = init_path + "/exploitdb/" + exploit.file
    try:
        with open(file_path, 'r') as f:
            content = f.readlines()
            vulnerability_code = ''.join(content)
        return render_template('code_viewer.html', vulnerability_code=vulnerability_code,
                               vulnerability_description=exploit.description, vulnerability_file=exploit.file,
                               vulnerability_author=exploit.author, vulnerability_date=exploit.date,
                               vulnerability_type=exploit.type, vulnerability_platform=exploit.platform,
                               vulnerability_port=exploit.port, file_path=file_path, exploit_id=exploit_id)
    except FileNotFoundError:
        error_msg = 'Sorry! This file does not exist :('
        return render_template('error_page.html', error=error_msg)


@app.route('/download-exploit')
def download_exploit_details():
    """
    Download the selected exploit.
    :return: a template showing the details about the selected exploit and the source code.
    """
    exploit_id = request.args.get('exploit-id', None)
    exploit = get_exploit_by_id(exploit_id)
    file_path = init_path + "/exploitdb/" + exploit.file
    try:
        with open(file_path, 'r') as f:
            content = f.readlines()
            vulnerability_code = ''.join(content)
        copyfile(file_path, os.path.expanduser("~") + "/exploit_" + exploit_id + get_vulnerability_extension(exploit.file))
        download_alert = "exploit_" + exploit_id + get_vulnerability_extension(exploit.file) + " has been downloaded in your home directory"
        return render_template('code_viewer.html', vulnerability_code=vulnerability_code,
                               vulnerability_description=exploit.description, vulnerability_file=exploit.file,
                               vulnerability_author=exploit.author, vulnerability_date=exploit.date,
                               vulnerability_type=exploit.type, vulnerability_platform=exploit.platform,
                               vulnerability_port=exploit.port, file_path=file_path, download_alert=download_alert,
                               exploit_id=exploit_id)
    except FileNotFoundError:
        error_msg = 'Sorry! This file does not exist :('
        return render_template('error_page.html', error=error_msg)


@app.route('/shellcode-details')
def view_shellcode_details():
    """
    Open details about the selected shellcode, included the source code.
    :return: a template showing the details about the selected shellcode and the source code.
    """
    shellcode_id = request.args.get('shellcode-id', None)
    shellcode = get_shellcode_by_id(shellcode_id)
    file_path = init_path + "/exploitdb/" + shellcode.file
    try:
        with open(file_path, 'r') as f:
            content = f.readlines()
            vulnerability_code = ''.join(content)
        return render_template('code_viewer.html', vulnerability_code=vulnerability_code,
                               vulnerability_description=shellcode.description, vulnerability_file=shellcode.file,
                               vulnerability_author=shellcode.author, vulnerability_date=shellcode.date,
                               vulnerability_type=shellcode.type, vulnerability_platform=shellcode.platform,
                               file_path=file_path, shellcode_id=shellcode_id)
    except FileNotFoundError:
        error_msg = 'Sorry! This file does not exist :('
        return render_template('error_page.html', error=error_msg)


@app.route('/download-shellcode')
def download_shellcode():
    """
    Download the selected shellcode.
    :return: a template showing the details about the selected shellcode and the source code.
    """
    shellcode_id = request.args.get('shellcode-id', None)
    shellcode = get_shellcode_by_id(shellcode_id)
    file_path = init_path + "/exploitdb/" + shellcode.file
    try:
        with open(file_path, 'r') as f:
            content = f.readlines()
            vulnerability_code = ''.join(content)
        copyfile(file_path, os.path.expanduser("~") + "/shellcode_" + shellcode_id + get_vulnerability_extension(shellcode.file))
        download_alert = "shellcode_" + shellcode_id + get_vulnerability_extension(shellcode.file) + " has been downloaded in your home directory"
        return render_template('code_viewer.html', vulnerability_code=vulnerability_code,
                               vulnerability_description=shellcode.description, vulnerability_file=shellcode.file,
                               vulnerability_author=shellcode.author, vulnerability_date=shellcode.date,
                               vulnerability_type=shellcode.type, vulnerability_platform=shellcode.platform,
                               file_path=file_path, download_alert=download_alert, shellcode_id=shellcode_id)
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



def start_app():
    # app.run(debug=True, host='0.0.0.0')
    app.run(debug=False)
