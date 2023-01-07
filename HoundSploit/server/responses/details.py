from flask import render_template
from HoundSploit.searcher.utils.vulnerability import get_vulnerability_file_path, get_vulnerability_code
from HoundSploit.searcher.engine.bookmarks import is_bookmarked


def render_vulnerability_details(vulnerability, is_prev_page_bookmarks, download_alert):
    if vulnerability.type == 'shellcode':
        vulnerability_class = 'shellcode'
    else:
        vulnerability_class = 'exploit'
    if vulnerability is not None:
        file_path = get_vulnerability_file_path(vulnerability)
        vulnerability_code = get_vulnerability_code(file_path)
        if vulnerability_code is not None:
            return render_template('code_viewer.html', vulnerability_code=vulnerability_code,
                            vulnerability=vulnerability, file_path=file_path,
                            bookmarked=is_bookmarked(vulnerability.id, vulnerability_class),
                            is_prev_page_bookmarks=is_prev_page_bookmarks,
                            download_alert=download_alert)
        else:
            error_msg = 'Sorry! This file does not exist :('
            return render_template('error_page.html', error=error_msg)
    else:
        error_msg = 'Sorry! This ' + vulnerability_class + ' does not exist :('
        return render_template('error_page.html', error=error_msg)
