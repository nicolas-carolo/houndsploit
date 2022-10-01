from HoundSploit.searcher.entities.suggestion import Suggestion
from HoundSploit.searcher.db_manager.session_manager import start_session
from HoundSploit.searcher.db_manager.result_set import queryset2list
from HoundSploit.searcher.utils.file import check_file_existence
from HoundSploit.searcher.utils.csv import add_suggestion_to_csv, delete_suggestion_from_csv,\
    edit_suggestion_in_csv

DEFAULT_SUGGESTIONS = ["joomla", "linux", "phpbb", "macos", "mac os x", "html 5", "wordpress"]


def substitute_with_suggestions(searched_text):
    suggestions_list = get_suggestions_list()
    for suggested_word in suggestions_list:
        if suggested_word.is_eligible(searched_text) and suggested_word.autoreplacement == 'true':
            searched_text = suggested_word.replace_searched_text_with_suggestion(searched_text)
    return searched_text


def propose_suggestions(searched_text):
    suggested_searched_text = ""
    suggestions_list = get_suggestions_list()
    for suggested_word in suggestions_list:
        if suggested_word.is_eligible(searched_text) and suggested_word.autoreplacement == 'false':
            suggested_searched_text = suggested_word.replace_searched_text_with_suggestion(searched_text)
    return suggested_searched_text


def get_suggestions_list():
    session = start_session()
    queryset = session.query(Suggestion)
    suggestions_list = queryset2list(queryset)
    session.close()
    return suggestions_list


def new_suggestion(searched, suggestion, autoreplacement):
    session = start_session()
    searched = str(searched).lower()
    suggestion = str(suggestion).lower()
    queryset = session.query(Suggestion).filter(Suggestion.searched == searched)
    results_list = queryset2list(queryset)
    if len(results_list) == 0:
        new_suggestion = Suggestion(searched, suggestion, autoreplacement)
        session.add(new_suggestion)
        add_suggestion_to_csv(searched, suggestion, autoreplacement)
    else:
        edited_suggestion = session.query(Suggestion).get(searched)
        edited_suggestion.suggestion = suggestion
        edited_suggestion.autoreplacement = autoreplacement
        edit_suggestion_in_csv(searched, suggestion, autoreplacement)
    session.commit()
    session.close()


def remove_suggestion(searched):
    session = start_session()
    suggestion_item = session.query(Suggestion).get(searched)
    if suggestion_item is not None:
        session.query(Suggestion).filter(Suggestion.searched == searched).delete()
        session.commit()
        session.close()
        delete_suggestion_from_csv(searched)
        return True
    else:
        session.close()
        return False
