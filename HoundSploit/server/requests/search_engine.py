from flask import request


def get_searched_text(request):
    if request.method == 'POST':
        searched_text = request.form['searched-text']
    else:
        searched_text = request.args.get('searched-text', None)
    if searched_text is None:
        searched_text = ""
    return searched_text


def is_previous_page_bookmarks(request):
    is_prev_page_bookmarks = request.args.get('isprevpagebookmarks', None)
    if is_prev_page_bookmarks == "true":
        return True
    else:
        return False


def get_current_exploits_page(request):
    if request.method == 'POST':
        current_exploits_page = request.form['hid-e-page']
        try:
            current_exploits_page = int(current_exploits_page)
        except ValueError:
            current_exploits_page = 1
        return current_exploits_page


def get_current_shellcodes_page(request):
    if request.method == 'POST':
        current_shellcodes_page = request.form['hid-s-page']
        try:
            current_shellcodes_page = int(current_shellcodes_page)
        except ValueError:
            current_shellcodes_page = 1
        return current_shellcodes_page


def get_current_results_view(request):
    if request.method == 'POST':
        current_view = request.form['current-view']
        return current_view


def get_sorting_type(request):
    if request.method == 'POST':
        sorting_type = request.form['sorting-type']
        return sorting_type
