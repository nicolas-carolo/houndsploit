import re


def str_contains_num_version(str):
    return bool(re.search(r' \d+((\.\d+)+)?', str))


def str_is_num_version(str):
    return bool(re.search(r'\d+((\.\d+)+)?', str))


def str_contains_software_name_and_num_version(text):
    if str_contains_num_version(str(text)) and str(text).__contains__(' ') and not str(text).__contains__('<'):
        return True
    else:
        return False


def str_contains_num_version_range(str):
    return bool(re.search(r'\d+((\.\d+)+)? < \d+((\.\d+)+)?', str))


def str_contains_num_version_range_with_x(str):
    return bool(re.search(r'\d+((\.\d+)+)?(\.x)? < \d+((\.\d+)+)?(\.x)?', str))


def string_contains(text_string, text_substring):
    if text_string.lower().__contains__(text_substring.lower()):
        return True
    else:
        return False


def highlight_keywords(keywords_list, text):
    description = str(text).upper()
    for keyword in keywords_list:
        if description.__contains__(keyword) and keyword != '<':
            regex = re.compile(re.escape(keyword), re.IGNORECASE)
            text = regex.sub("<span class='keyword'>" + keyword + '</span>', text)
    return text