from searcher.models import Exploit


def search_exploits_in_db(search_text):
    if is_number(search_text):
        search_string = 'select * from exploits where ' + 'id = ' + search_text + ' or file like \'%' + search_text + '%\' or description like \'%' + search_text + '%\' or port = ' + search_text
    else:
        search_string = 'select * from exploits where ' + 'file like \'%' + search_text + '%\' or description like \'%' + search_text + '%\' or author like \'%' + search_text + '\' or platform like \'%' + search_text + '%\''
    print(search_string)
    return Exploit.objects.raw(search_string)


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False
