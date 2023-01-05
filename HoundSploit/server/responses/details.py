from flask import render_template
from HoundSploit.searcher.utils.constants import BASE_DIR
from HoundSploit.searcher.engine.bookmarks import is_bookmarked

def render_exploit_details(exploit, is_prev_page_bookmarks):
    if exploit is not None:
        file_path = get_vulnerability_file_path(exploit)
        vulnerability_code = get_vulnerability_code(file_path)
        if vulnerability_code is not None:
            #return render_template('code_viewer.html', vulnerability_code=vulnerability_code,
            #                vulnerability_description=exploit.description, vulnerability_file=exploit.file,
            #                vulnerability_author=exploit.author, vulnerability_date=exploit.date,
            #                vulnerability_type=exploit.type, vulnerability_platform=exploit.platform,
            #                vulnerability_port=exploit.port, file_path=file_path, exploit_id=exploit.id,
            #                bookmarked=is_bookmarked(exploit.id, 'exploit'),
            #                searched_text=searched_text, is_prev_page_bookmarks=is_prev_page_bookmarks)
            return render_template('code_viewer.html', vulnerability_code=vulnerability_code,
                            vulnerability=exploit, file_path=file_path,
                            bookmarked=is_bookmarked(exploit.id, 'exploit'),
                            is_prev_page_bookmarks=is_prev_page_bookmarks)
        else:
            error_msg = 'Sorry! This file does not exist :('
            return render_template('error_page.html', error=error_msg)
    else:
        error_msg = 'Sorry! This exploit does not exist :('
        return render_template('error_page.html', error=error_msg)


def render_shellcode_details(shellcode, is_prev_page_bookmarks):
    if shellcode is not None:
        file_path = get_vulnerability_file_path(shellcode)
        vulnerability_code = get_vulnerability_code(file_path)
        if vulnerability_code is not None:
            return render_template('code_viewer.html', vulnerability_code=vulnerability_code,
                            vulnerability=shellcode, file_path=file_path,
                            bookmarked=is_bookmarked(shellcode.id, 'shellcode'),
                            is_prev_page_bookmarks=is_prev_page_bookmarks)
        else:
            error_msg = 'Sorry! This file does not exist :('
            return render_template('error_page.html', error=error_msg)
    else:
        error_msg = 'Sorry! This shellcode does not exist :('
        return render_template('error_page.html', error=error_msg)


def get_vulnerability_code(file_path):
    try:
        with open(file_path, 'r') as f:
            content = f.readlines()
            vulnerability_code = ''.join(content)
    except FileNotFoundError:
        vulnerability_code = None
    return vulnerability_code


def get_vulnerability_file_path(vulnerability):
    file_path = BASE_DIR + "/exploitdb/" + vulnerability.file
    return file_path