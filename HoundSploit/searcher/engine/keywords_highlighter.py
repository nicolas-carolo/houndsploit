from HoundSploit.searcher.utils.string import highlight_keywords


def highlight_keywords_in_description(keywords_list, vulnerabilities_list):
    for vulnerability in vulnerabilities_list:
        vulnerability.description = highlight_keywords(keywords_list, vulnerability.description)
    return vulnerabilities_list


def highlight_keywords_in_file(keywords_list, vulnerabilities_list):
    for vulnerability in vulnerabilities_list:
        vulnerability.file = highlight_keywords(keywords_list, vulnerability.file)
    return vulnerabilities_list


def highlight_keywords_in_author(keywords_list, vulnerabilities_list):
    for vulnerability in vulnerabilities_list:
        vulnerability.author = highlight_keywords(keywords_list, vulnerability.author)
    return vulnerabilities_list


def highlight_keywords_in_port(keywords_list, vulnerabilities_list):
    for exploit in vulnerabilities_list:
        exploit.port = highlight_keywords(keywords_list, exploit.port)
    return vulnerabilities_list
