from django.shortcuts import render
from searcher.engine.search_engine import search_vulnerabilities_in_db, search_vulnerabilities_advanced,\
    substitute_with_suggestions, propose_suggestions
from searcher.models import Exploit, Shellcode
import os
import re
from searcher.forms import AdvancedSearchForm, SimpleSearchForm
from searcher.forms import OPERATOR_CHOICES, get_type_values, get_platform_values
from searcher.engine.date_validator import is_date_range_valid
import datetime


def get_results_table(request):
    """
    Render a table with a list of search results.
    :param request: the HTTP request.
    :return: results_table.html template with search results.
    """
    if request.POST:
        form = SimpleSearchForm(request.POST)
        if form.is_valid():
            user_input = form.cleaned_data['search_text']
            search_text = substitute_with_suggestions(user_input)
            suggested_search_text = propose_suggestions(user_input)
            exploits_results = search_vulnerabilities_in_db(search_text, 'searcher_exploit')
            for result in exploits_results:
                if result.port is None:
                    result.port = ''
            shellcodes_results = search_vulnerabilities_in_db(search_text, 'searcher_shellcode')
            return render(request, "results_table.html", {'form': form,
                                                          'searched_item': str(search_text),
                                                          'exploits_results': exploits_results,
                                                          'n_exploits_results': len(exploits_results),
                                                          'shellcodes_results': shellcodes_results,
                                                          'n_shellcodes_results': len(shellcodes_results),
                                                          'suggested_search_text': suggested_search_text
                                                          })
        else:
            form = SimpleSearchForm()
            return render(request, 'home.html', {'form': form})
    else:
        form = SimpleSearchForm()
        return render(request, 'home.html', {'form': form})


def view_exploit_code(request, exploit_id):
    """
    Open details about the selected exploit, included the source code.
    :param request: the HTTP request.
    :param exploit_id: the ID of the exploit we want to open.
    :return: a template showing the details about the selected exploit and the source code.
    """
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
                                                    'type': exploit.type,
                                                    'vulnerability_platform': exploit.platform,
                                                    'vulnerability_port': exploit.port,
                                                    'file_path': file_path,
                                                    'file_name': exploit.description
                                                    + get_vulnerability_extension(exploit.file),
                                                    })
    except FileNotFoundError:
        error_msg = 'Sorry! This file does not exist :('
        return render(request, 'error_page.html', {'error': error_msg})


def view_shellcode_code(request, shellcode_id):
    """
    Open details about the selected shellcode, included the source code.
    :param request: the HTTP request.
    :param shellcode_id: the ID of the shellcode we want to open.
    :return: a template showing the details about the selected shellcode and the source code.
    """
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
                                                    'type': shellcode.type,
                                                    'vulnerability_platform': shellcode.platform,
                                                    'file_path': file_path,
                                                    'file_name': shellcode.description
                                                    + get_vulnerability_extension(shellcode.file),
                                                    })
    except FileNotFoundError:
        error_msg = 'Sorry! This file does not exist :('
        return render(request, 'error_page.html', {'error': error_msg})


def show_help(request):
    """
    Render a template containing some information about the use of HoundSploit.
    :param request: the HTTP request.
    :return: a template containing some information about the use of HoundSploit.
    """
    return render(request, 'help.html')


def show_info(request):
    """
    Render a template containing some information about the current version of HoundSploit.
    :param request: the HTTP request.
    :return: a template containing some information about the current version of HoundSploit.
    """
    return render(request, 'about.html')


def get_vulnerability_extension(vulnerability_file):
    """
    Get the extension of the vulnerability passed as parameter.
    :param vulnerability_file: the vulnerability we want to get its extension.
    :return: the extension of the vulnerability passed as parameter.
    """
    regex = re.search(r'\.(?P<extension>\w+)', vulnerability_file)
    extension = '.' + regex.group('extension')
    return extension


def get_results_table_advanced(request):
    """
    Render a table with a list of advanced search results.
    :param request: the HTML request.
    :return: advanced_results_table.html template with advanced search results.
    """
    if request.POST:
        form = AdvancedSearchForm(request.POST)
        if form.is_valid() and is_date_range_valid(form.cleaned_data['start_date'], form.cleaned_data['end_date']):
            user_input = form.cleaned_data['search_text']
            search_text = substitute_with_suggestions(user_input)
            suggested_search_text = propose_suggestions(user_input)
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

            relative_suggested_link = None
            if not suggested_search_text == '':
                relative_suggested_link = suggested_search_text + '/' + str(operator_filter_index)\
                                          + '/' + str(type_filter_index) + '/' + str(platform_filter_index) + '/'\
                                          + author_filter + '/' + str(port_filter) + '/' + str(start_date_filter) + '/'\
                                          + str(end_date_filter)

            exploits_results = search_vulnerabilities_advanced(search_text,'searcher_exploit', operator_filter,
                                                               type_filter, platform_filter, author_filter, port_filter,
                                                               start_date_filter, end_date_filter)
            shellcodes_results = search_vulnerabilities_advanced(search_text, 'searcher_shellcode', operator_filter,
                                                                 type_filter, platform_filter, author_filter,
                                                                 port_filter, start_date_filter, end_date_filter)

            for result in exploits_results:
                if result.port is None:
                    result.port = ''

            return render(request, 'advanced_results_table.html', {'form': form,
                                                                   'searched_item': str(search_text),
                                                                   'exploits_results': exploits_results,
                                                                   'n_exploits_results': len(exploits_results),
                                                                   'shellcodes_results': shellcodes_results,
                                                                   'n_shellcodes_results': len(shellcodes_results),
                                                                   'suggested_search_text': suggested_search_text,
                                                                   'relative_suggested_link': relative_suggested_link
                                                                   })
        else:
            form = AdvancedSearchForm()
            return render(request, 'advanced_searcher.html', {'form': form,
                                                              'date_range_error': 'ERROR: Bad date range!'
                                                              })
    else:
        form = AdvancedSearchForm()
        return render(request, 'advanced_searcher.html', {'form': form})


def change_user_input(request, suggested_input):
    form = SimpleSearchForm()
    form.initial['search_text'] = suggested_input
    exploits_results = search_vulnerabilities_in_db(suggested_input, 'searcher_exploit')
    for result in exploits_results:
        if result.port is None:
            result.port = ''
    shellcodes_results = search_vulnerabilities_in_db(suggested_input, 'searcher_shellcode')
    return render(request, "results_table.html", {'form': form,
                                                  'searched_item': str(suggested_input),
                                                  'exploits_results': exploits_results,
                                                  'n_exploits_results': len(exploits_results),
                                                  'shellcodes_results': shellcodes_results,
                                                  'n_shellcodes_results': len(shellcodes_results)
                                                  })


def change_user_input_advanced(request, suggested_input, operator_index, type_index, platform_index, author, port,
                               start_date, end_date):
    form = AdvancedSearchForm(initial={'operator': int(operator_index), 'type': int(type_index),
                                       'platform': int(platform_index)})
    try:
        port_int = int(port)
    except ValueError:
        port_int = None

    try:
        start_date_filter = datetime.datetime.strptime(start_date, '%Y-%m-%d')
        end_date_filter = datetime.datetime.strptime(end_date, '%Y-%m-%d')
    except ValueError:
        start_date_filter = None
        end_date_filter = None

    form.initial['search_text'] = suggested_input
    form.initial['author'] = author
    form.initial['port'] = port_int
    form.initial['start_date'] = start_date
    form.initial['end_date'] = end_date

    operator_filter = OPERATOR_CHOICES.__getitem__(int(operator_index))[1]
    type_filter = get_type_values().__getitem__(int(type_index))[1]
    platform_filter = get_platform_values().__getitem__(int(platform_index))[1]
    author_filter = author
    port_filter = port_int

    exploits_results = search_vulnerabilities_advanced(suggested_input, 'searcher_exploit', operator_filter,
                                                       type_filter, platform_filter, author_filter, port_filter,
                                                       start_date_filter, end_date_filter)
    shellcodes_results = search_vulnerabilities_advanced(suggested_input, 'searcher_shellcode', operator_filter,
                                                         type_filter, platform_filter, author_filter,
                                                         port_filter, start_date_filter, end_date_filter)

    for result in exploits_results:
        if result.port is None:
            result.port = ''

    return render(request, "advanced_results_table.html", {'form': form,
                                                            'searched_item': str(suggested_input),
                                                            'exploits_results': exploits_results,
                                                            'n_exploits_results': len(exploits_results),
                                                            'shellcodes_results': shellcodes_results,
                                                            'n_shellcodes_results': len(shellcodes_results)
                                                            })

