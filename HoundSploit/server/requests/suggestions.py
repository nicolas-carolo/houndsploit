from flask import request


def get_searched_text_suggestion(request):
    if request.method == 'POST':
        searched_text_suggestion = request.form['searched']
        
    else:
        searched_text_suggestion = request.args.get('searched', None)
    return searched_text_suggestion


def get_search_suggestion(request):
    if request.method == 'POST':
        search_suggestion = request.form['suggestion']
        return search_suggestion


def get_suggestion_autoreplacement_flag(request):
    if request.method == 'POST':
        autoreplacement = request.form['autoreplacement']
        return autoreplacement