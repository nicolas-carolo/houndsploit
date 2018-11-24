from searcher.models import Exploit


def search_exploits_in_db(search_text):
    search_string = 'select * from exploits where ' + search_text
    print(search_string)
    for exploit in Exploit.objects.raw(search_string):
        print(exploit.id, exploit.file, exploit.description)
    return Exploit.objects.raw(search_string)