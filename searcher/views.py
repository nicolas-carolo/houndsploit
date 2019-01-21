from django.shortcuts import render
from searcher.engine.search_engine import search_vulnerabilities_in_db, search_vulnerabilities_advanced
from searcher.models import Exploit, Shellcode
import os
import re
from searcher.forms import AdvancedSearchForm, SimpleSearchForm
from searcher.forms import OPERATOR_CHOICES, get_type_values, get_platform_values


def get_results_table(request):
    if request.POST:
        form = SimpleSearchForm(request.POST)
        if form.is_valid():
            search_text = form.cleaned_data['search_text']
            return render(request, "results_table.html", {'form': form,
                                                          'searched_item': str(search_text),
                                                          'exploits_results': search_vulnerabilities_in_db(search_text, 'searcher_exploit'),
                                                          'n_exploits_results': len(search_vulnerabilities_in_db(search_text,'searcher_exploit')),
                                                          'shellcodes_results': search_vulnerabilities_in_db(search_text, 'searcher_shellcode'),
                                                          'n_shellcodes_results': len(search_vulnerabilities_in_db(search_text, 'searcher_shellcode'))
                                                          })
        else:
            form = SimpleSearchForm()
            return render(request, 'home.html', {'form': form})
    else:
        form = SimpleSearchForm()
        return render(request, 'home.html', {'form': form})


def view_exploit_code(request, exploit_id):
    exploit = Exploit.objects.get(id=exploit_id)
    pwd = os.path.dirname(__file__)
    file_path = '/static/vulnerabilities/' + exploit.file
    try:
        with open(pwd + '/static/vulnerabilities/' + exploit.file, 'r') as f:
            content = f.readlines()
            vulnerability_code = ''.join(content)
        return render(request, 'code_viewer.html', {'vulnerability_code': vulnerability_code,
                                                    'vulnerability_description': exploit.description,
                                                    'vulnerability_file': exploit.file,
                                                    'vulnerability_author': exploit.author,
                                                    'vulnerability_date': exploit.date,
                                                    'vulnerability_type': exploit.vulnerability_type,
                                                    'vulnerability_platform': exploit.platform,
                                                    'vulnerability_port': exploit.port,
                                                    'file_path': file_path,
                                                    'file_name': exploit.description + get_vulnerability_extension(exploit.file),
                                                    })
    except FileNotFoundError:
        error_msg = 'Sorry! This file does not exist :('
        return render(request, 'error_page.html', {'error': error_msg})


def view_shellcode_code(request, shellcode_id):
    shellcode = Shellcode.objects.get(id=shellcode_id)
    pwd = os.path.dirname(__file__)
    file_path = '/static/vulnerabilities/' + shellcode.file
    try:
        with open(pwd + '/static/vulnerabilities/' + shellcode.file, 'r') as f:
            content = f.readlines()
            vulnerability_code = ''.join(content)
        return render(request, 'code_viewer.html', {'vulnerability_code': vulnerability_code,
                                                    'vulnerability_description': shellcode.description,
                                                    'vulnerability_file': shellcode.file,
                                                    'vulnerability_author': shellcode.author,
                                                    'vulnerability_date': shellcode.date,
                                                    'vulnerability_type': shellcode.vulnerability_type,
                                                    'vulnerability_platform': shellcode.platform,
                                                    'file_path': file_path,
                                                    'file_name': shellcode.description + get_vulnerability_extension(shellcode.file),
                                                    })
    except FileNotFoundError:
        error_msg = 'Sorry! This file does not exist :('
        return render(request, 'error_page.html', {'error': error_msg})


def show_help(request):
    return render(request, 'help.html')


def show_info(request):
    return render(request, 'about.html')


def get_vulnerability_extension(vulnerability_file):
    regex = re.search(r'\.(?P<extension>\w+)', vulnerability_file)
    extension = '.' + regex.group('extension')
    return extension


def get_results_table_advanced(request):
    if request.POST:
        form = AdvancedSearchForm(request.POST)
        if form.is_valid():
            search_text = form.cleaned_data['search_text']
            operator_filter_index = int(form.cleaned_data['operator'])
            operator_filter = OPERATOR_CHOICES.__getitem__(operator_filter_index)[1]
            type_filter_index = int(form.cleaned_data['type'])
            type_filter = get_type_values().__getitem__(type_filter_index)[1]
            platform_filter_index = int(form.cleaned_data['platform'])
            platform_filter = get_platform_values().__getitem__(platform_filter_index)[1]
            author_filter = form.cleaned_data['author']
            port_filter = form.cleaned_data['port']
            start_date_filter = form.cleaned_data['start_date']
            end_date_filter = form.cleaned_data['end_date']

            func_exploits = search_vulnerabilities_advanced(search_text,'searcher_exploit', operator_filter, type_filter, platform_filter, author_filter, port_filter, start_date_filter, end_date_filter)
            func_shellcodes = search_vulnerabilities_advanced(search_text, 'searcher_shellcode', operator_filter, type_filter, platform_filter, author_filter, port_filter, start_date_filter, end_date_filter)
            return render(request, 'advanced_results_table.html', {'form': form,
                                                                   'searched_item': str(search_text),
                                                                   'exploits_results': func_exploits,
                                                                   'n_exploits_results': len(func_exploits),
                                                                   'shellcodes_results': func_shellcodes,
                                                                   'n_shellcodes_results': len(func_shellcodes)
                                                                   })
        else:
            form = AdvancedSearchForm()
            return render(request, 'advanced_searcher.html', {'form': form})
    else:
        form = AdvancedSearchForm()
        return render(request, 'advanced_searcher.html', {'form': form})
