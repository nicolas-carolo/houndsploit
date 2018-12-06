from django.shortcuts import render
from searcher.search_engine import search_vulnerabilities_in_db
from searcher.search_engine import is_valid_input
from searcher.models import Exploit, Shellcode
import os


def get_results_table(request):
    if request.POST and is_valid_input(request.POST['search_item']):
        search_text = request.POST['search_item']
        return render(request, "results_table.html", {'searched_item': str(search_text),
                                                      'exploits_results': search_vulnerabilities_in_db(search_text, 'searcher_exploit'),
                                                      'n_exploits_results': len(search_vulnerabilities_in_db(search_text, 'searcher_exploit')),
                                                      'shellcodes_results': search_vulnerabilities_in_db(search_text, 'searcher_shellcode'),
                                                      'n_shellcodes_results': len(search_vulnerabilities_in_db(search_text, 'searcher_shellcode'))
                                                      })
    else:
        return render(request, 'home.html')


def view_exploit_code(request, exploit_id):
    exploit = Exploit.objects.get(id=exploit_id)
    pwd = os.path.dirname(__file__)
    file = open(pwd + '/static/vulnerability/' + exploit.file, 'r')
    vulnerability_code = ''
    for line in file:
        vulnerability_code = vulnerability_code + line
    return render(request, 'code_viewer.html', {'vulnerability_code': vulnerability_code})


def view_shellcode_code(request, shellcode_id):
    shellcode = Shellcode.objects.get(id=shellcode_id)
    pwd = os.path.dirname(__file__)
    file = open(pwd + '/static/vulnerability/' + shellcode.file, 'r')
    vulnerability_code = ''
    for line in file:
        vulnerability_code = vulnerability_code + line
    return render(request, 'code_viewer.html', {'vulnerability_code': vulnerability_code})



