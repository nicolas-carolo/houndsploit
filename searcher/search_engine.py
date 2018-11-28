from searcher.models import Exploit


def search_exploits_in_db(search_text):
    if is_number(search_text):
        search_string = 'select * from exploits where ' + 'id = ' + search_text + ' or file like \'%' + search_text + '%\' or description like \'%' + search_text + '%\' or port = ' + search_text
    else:
        words_list = str(search_text).split()
        search_concat_text = '%'
        for word in words_list:
            search_concat_text = search_concat_text + word.upper() + '%'
        search_string = 'select * from exploits where ' + '(file like \'' + search_concat_text  + '\' or author like \'' + search_concat_text + '\' or exploit_type like \'' + search_concat_text + '\' or platform like \'' + search_concat_text + '\') or (description like \'%' + words_list[0].upper() + '%\''
        for word in words_list[1:]:
            search_string = search_string + ' and description like \'%' + word.upper() + '%\''
        search_string = search_string + ')'
    print(search_string)
    return Exploit.objects.raw(search_string)


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False
