from flask import render_template
from HoundSploit.searcher.utils.vulnerability import get_vulnerability_file_path, get_vulnerability_code
from HoundSploit.searcher.engine.bookmarks import is_bookmarked

def render_exploit_details(exploit, is_prev_page_bookmarks, download_alert):
    if exploit is not None:
        file_path = get_vulnerability_file_path(exploit)
        vulnerability_code = get_vulnerability_code(file_path)
        if vulnerability_code is not None:
            return render_template('code_viewer.html', vulnerability_code=vulnerability_code,
                            vulnerability=exploit, file_path=file_path,
                            bookmarked=is_bookmarked(exploit.id, 'exploit'),
                            is_prev_page_bookmarks=is_prev_page_bookmarks,
                            download_alert=download_alert)
        else:
            error_msg = 'Sorry! This file does not exist :('
            return render_template('error_page.html', error=error_msg)
    else:
        error_msg = 'Sorry! This exploit does not exist :('
        return render_template('error_page.html', error=error_msg)


def render_shellcode_details(shellcode, is_prev_page_bookmarks, download_alert):
    if shellcode is not None:
        file_path = get_vulnerability_file_path(shellcode)
        vulnerability_code = get_vulnerability_code(file_path)
        if vulnerability_code is not None:
            return render_template('code_viewer.html', vulnerability_code=vulnerability_code,
                            vulnerability=shellcode, file_path=file_path,
                            bookmarked=is_bookmarked(shellcode.id, 'shellcode'),
                            is_prev_page_bookmarks=is_prev_page_bookmarks,
                            download_alert=download_alert)
        else:
            error_msg = 'Sorry! This file does not exist :('
            return render_template('error_page.html', error=error_msg)
    else:
        error_msg = 'Sorry! This shellcode does not exist :('
        return render_template('error_page.html', error=error_msg)
