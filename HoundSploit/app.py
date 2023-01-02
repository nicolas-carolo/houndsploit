from flask import Flask
from HoundSploit.searcher.utils.constants import BASE_DIR, TEMPLATE_DIR, STATIC_DIR
from HoundSploit.server.controller import request_search_results, request_advanced_search_results,\
    request_exploit_details, request_download_exploit, request_shellcode_details,\
    request_download_shellcode, request_settings, request_update, request_suggestions_manager,\
    request_add_suggestion, request_delete_suggestion, request_bookmarks_manager,\
    request_add_bookmark_exploit, request_delete_bookmark_exploit, request_add_bookmark_shellcode,\
    request_delete_bookmark_shellcode
    


app = Flask(__name__, template_folder=TEMPLATE_DIR, static_folder=STATIC_DIR)

@app.route('/', methods=['GET', 'POST'])
def get_results_table():
    return request_search_results()


@app.route('/advanced-search', methods=['GET', 'POST'])
def get_results_table_advanced():
    return request_advanced_search_results()


@app.route('/exploit-details')
def view_exploit_details():
    return request_exploit_details()


@app.route('/download-exploit')
def download_exploit():
    return request_download_exploit()


@app.route('/shellcode-details')
def view_shellcode_details():
    return request_shellcode_details()


@app.route('/download-shellcode')
def download_shellcode():
    return request_download_shellcode()


@app.route('/settings')
def settings():
    return request_settings()


@app.route('/update')
def get_updates():
    return request_update()


@app.route('/suggestions')
def open_suggestions_manager():
    return request_suggestions_manager()


@app.route('/add-suggestion', methods=['GET', 'POST'])
def add_suggestion():
    return request_add_suggestion()


@app.route('/delete-suggestion')
def delete_suggestion():
    return request_delete_suggestion()


@app.route('/bookmarks', methods=['GET', 'POST'])
def open_bookmarks_manager():
    return request_bookmarks_manager()


@app.route('/bookmark-exploit')
def add_bookmark_exploit():
    return request_add_bookmark_exploit()


@app.route('/remove-bookmark-exploit')
def delete_bookmark_exploit():
    return request_delete_bookmark_exploit()


@app.route('/bookmark-shellcode')
def add_bookmark_shellcode():
    return request_add_bookmark_shellcode()


@app.route('/remove-bookmark-shellcode')
def delete_bookmark_shellcode():
    return request_delete_bookmark_shellcode()


def start_app():
    # app.run(debug=True, host='0.0.0.0')
    app.run(debug=False)
