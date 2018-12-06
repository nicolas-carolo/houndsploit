from django.shortcuts import render, redirect
from searcher.search_engine import search_vulnerabilities_in_db
from searcher.search_engine import is_valid_input


def get_results_table(request):
    if request.POST and is_valid_input(request.POST['search_item']):
        search_text = request.POST['search_item']
        return render(request, "results_table.html", {'searched_item': str(search_text),
                                                      'exploits_results': search_vulnerabilities_in_db(search_text, 'exploits'),
                                                      'n_exploits_results': len(search_vulnerabilities_in_db(search_text, 'exploits')),
                                                      'shellcodes_results': search_vulnerabilities_in_db(search_text, 'shellcodes'),
                                                      'n_shellcodes_results': len(search_vulnerabilities_in_db(search_text, 'shellcodes'))
                                                      })
    else:
        return render(request, 'home.html')


def view_code(request, id):
    print('It works!')
    return render(request, 'code_viewer.html', {'vulnerability_id': id})



