import os
import sys
import datetime

from flask import Flask, render_template, request
from HoundSploit.searcher.engine.search_engine import search_vulnerabilities_in_db, get_exploit_by_id, get_shellcode_by_id,\
    get_vulnerability_extension, get_vulnerability_filters, search_vulnerabilities_advanced
from HoundSploit.searcher.engine.keywords_highlighter import highlight_keywords_in_description, highlight_keywords_in_file, \
    highlight_keywords_in_port
from HoundSploit.searcher.engine.suggestions import substitute_with_suggestions, propose_suggestions, get_suggestions_list,\
    new_suggestion, remove_suggestion
from HoundSploit.searcher.engine.updates import get_latest_db_update_date, install_updates
from HoundSploit.searcher.engine.utils import check_file_existence
from HoundSploit.searcher.engine.csv2sqlite import create_db


init_path = os.path.expanduser("~") + "/HoundSploit"
template_dir = os.path.abspath(init_path + '/houndsploit/HoundSploit/templates')
static_folder = os.path.abspath(init_path + '/houndsploit/HoundSploit/static')
app = Flask(__name__, template_folder=template_dir, static_folder=static_folder)


@app.route('/', methods=['GET', 'POST'])
def get_results_table():
    """
    Render a table with a list of search results.
    :return: results_table.html template with search results.
    """
    if request.method == 'POST':
        searched_text = request.form['searched-text']
        searched_text = substitute_with_suggestions(searched_text)
        suggested_search_text = propose_suggestions(searched_text)
        if str(searched_text).isspace() or searched_text == "":
            return render_template('home.html')
        key_words_list = (str(searched_text).upper()).split()
        exploits_list = search_vulnerabilities_in_db(searched_text, 'searcher_exploit')
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
                               searched_text=searched_text, suggested_search_text=suggested_search_text)
    else:
        return render_template('home.html')


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

        try:
            date_from = datetime.datetime.strptime(date_from_filter, '%Y-%m-%d')
            date_to = datetime.datetime.strptime(date_to_filter, '%Y-%m-%d')
            if date_from > date_to:
                date_from_filter = "mm/dd/yyyy"
                date_to_filter = "mm/dd/yyyy"
                # TODO implement javascript error
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
                               vulnerability_platforms_list=vulnerability_platforms_list, author_filter=author_filter,
                               type_filter=type_filter, platform_filter=platform_filter, port_filter=port_filter,
                               date_from_filter=date_from_filter, date_to_filter=date_to_filter,
                               suggested_search_text=suggested_search_text)
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
        file_name = exploit.description + get_vulnerability_extension(exploit.file)
        return render_template('code_viewer.html', vulnerability_code=vulnerability_code,
                               vulnerability_description=exploit.description, vulnerability_file=exploit.file,
                               vulnerability_author=exploit.author, vulnerability_date=exploit.date,
                               vulnerability_type=exploit.type, vulnerability_platform=exploit.platform,
                               vulnerability_port=exploit.port, file_path=file_path, file_name=file_name)
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
        file_name = shellcode.description + get_vulnerability_extension(shellcode.file)
        return render_template('code_viewer.html', vulnerability_code=vulnerability_code,
                               vulnerability_description=shellcode.description, vulnerability_file=shellcode.file,
                               vulnerability_author=shellcode.author, vulnerability_date=shellcode.date,
                               vulnerability_type=shellcode.type, vulnerability_platform=shellcode.platform,
                               file_path=file_path, file_name=file_name)
    except FileNotFoundError:
        error_msg = 'Sorry! This file does not exist :('
        return render_template('error_page.html', error=error_msg)


@app.route('/about')
def about():
    """
    Show software information
    :return: about templates
    """
    return render_template('about.html', latest_db_update=get_latest_db_update_date())


@app.route('/update')
def get_updates():
    """
    Check and download new updates for the software and the database
    :return: about templates
    """
    install_updates()
    if check_file_existence(init_path + "/houndsploit_db.lock"):
        if check_file_existence(init_path + "/hound_db.sqlite3"):
            os.remove(init_path + "/hound_db.sqlite3")
        create_db()
    return render_template('about.html', latest_db_update=get_latest_db_update_date())


@app.route('/suggestions')
def suggestions_manager():
    """
    Open suggestions manager
    :return: suggestion manager template
    """
    return render_template('suggestions.html', suggestions=get_suggestions_list())


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
        new_suggestion(searched, suggestion, autoreplacement)
    return render_template('suggestions.html', suggestions=get_suggestions_list())


@app.route('/delete-suggestion')
def delete_suggestion():
    """
    Delete a suggestion selected by the user.
    :return: the 'suggestions.html' template. In case of error it shows an error message.
    """
    searched = request.args.get('searched', None)
    if remove_suggestion(searched):
        return render_template('suggestions.html', suggestions=get_suggestions_list())
    else:
        error = 'ERROR: The suggestion you want to delete does not exist!'
        return render_template('suggestions.html', suggestions=get_suggestions_list(), suggestion_error=error)



def start_app():
    app.run(debug=True, host='0.0.0.0')
