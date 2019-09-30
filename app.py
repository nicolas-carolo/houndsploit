import os

from flask import Flask, render_template, request
from searcher.engine.search_engine import search_vulnerabilities_in_db, get_exploit_by_id, get_shellcode_by_id,\
    get_vulnerability_extension, get_vulnerability_filters, search_vulnerabilities_advanced

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def get_results_table():
    """
    Render a table with a list of search results.
    :return: results_table.html template with search results.
    """
    if request.method == 'POST':
        searched_text = request.form['searched-text']
        exploits_list = search_vulnerabilities_in_db(searched_text, 'searcher_exploit')
        for result in exploits_list:
            if result.port is None:
                result.port = ''
        shellcodes_list = search_vulnerabilities_in_db(searched_text, 'searcher_shellcode')
        return render_template('results_table.html', searched_item=searched_text,
                               exploits_list=exploits_list, shellcodes_list=shellcodes_list,
                               searched_text=searched_text)
    else:
        return render_template('home.html')


@app.route('/advanced-search', methods=['GET', 'POST'])
def get_results_table_advanced():
    """
    Render a table with a list of search results.
    :return: results_table.html template with search results.
    """
    if request.method == 'POST':
        searched_text = request.form['searched-text']
        operator_filter = request.form['search-operator']
        author_filter = request.form['author']
        type_filter = request.form['type']
        platform_filter = request.form['platform']
        port_filter = request.form['port']
        date_from_filter = request.form['date-from']
        date_to_filter = request.form['date-to']
        exploits_list = search_vulnerabilities_advanced(searched_text, 'searcher_exploit', operator_filter, type_filter,
                                                        platform_filter, author_filter, port_filter, date_from_filter,
                                                        date_to_filter)
        for result in exploits_list:
            if result.port is None:
                result.port = ''
        shellcodes_list = search_vulnerabilities_advanced(searched_text, 'searcher_shellcode', operator_filter,
                                                          type_filter, platform_filter, author_filter, port_filter,
                                                          date_from_filter, date_to_filter)
        return render_template('advanced_results_table.html', searched_item=searched_text,
                               exploits_list=exploits_list, shellcodes_list=shellcodes_list,
                               searched_text=searched_text)
    else:
        vulnerability_types_list, vulnerability_platforms_list = get_vulnerability_filters()
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
    pwd = os.path.dirname(__file__)
    file_path = '/static/vulnerabilities/' + exploit.file
    try:
        with open(pwd + '/static/vulnerabilities/' + exploit.file, 'r') as f:
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
    pwd = os.path.dirname(__file__)
    file_path = '/static/vulnerabilities/' + shellcode.file
    try:
        with open(pwd + '/static/vulnerabilities/' + shellcode.file, 'r') as f:
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


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
