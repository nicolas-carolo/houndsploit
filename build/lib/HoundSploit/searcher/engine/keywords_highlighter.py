import re


def highlight_keywords_in_description(keywords_list, vulnerabilities_list):
    """
    Highlight searched keywords in the 'description' field.
    :param keywords_list: the list of keywords typed by the user in the search field.
    :param vulnerabilities_list: the list containing all the search results.
    :return: a queryset containing all search results formatted with HTML code for highlighting searched keywords.
    """
    for vulnerability in vulnerabilities_list:
        for keyword in keywords_list:
            if keyword != '<':
                description = str(vulnerability.description).upper()
                if description.__contains__(keyword):
                    regex = re.compile(re.escape(keyword), re.IGNORECASE)
                    vulnerability.description = regex.sub("<span class='keyword'>" + keyword + '</span>',
                                                          vulnerability.description)
    return vulnerabilities_list


def highlight_keywords_in_file(keywords_list, vulnerabilities_list):
    """
    Highlight searched keywords in the 'file' field.
    :param keywords_list: the list of keywords typed by the user in the search field.
    :param vulnerabilities_list: the list containing all the search results.
    :return: a queryset containing all search results formatted with HTML code for highlighting searched keywords.
    """
    for vulnerability in vulnerabilities_list:
        for keyword in keywords_list:
            file = str(vulnerability.file).upper()
            if file.__contains__(keyword):
                regex = re.compile(re.escape(keyword), re.IGNORECASE)
                vulnerability.file = regex.sub("<span class='keyword'>" + keyword + '</span>', vulnerability.file)
    return vulnerabilities_list


def highlight_keywords_in_author(keywords_list, vulnerabilities_list):
    """
    Highlight searched keywords in the 'author' field.
    :param keywords_list: the list of keywords typed by the user in the search field.
    :param vulnerabilities_list: the list containing all the search results.
    :return: a queryset containing all search results formatted with HTML code for highlighting searched keywords.
    """
    for vulnerability in vulnerabilities_list:
        for keyword in keywords_list:
            file = str(vulnerability.author).upper()
            if file.__contains__(keyword):
                regex = re.compile(re.escape(keyword), re.IGNORECASE)
                vulnerability.author = regex.sub("<span class='keyword'>" + keyword + '</span>', vulnerability.author)
    return vulnerabilities_list


def highlight_keywords_in_port(keywords_list, vulnerabilities_list):
    """
    Highlight searched keywords in the 'port' field.
    :param keywords_list: the list of keywords typed by the user in the search field.
    :param vulnerabilities_list: the list containing all the search results.
    :return: a queryset containing all search results formatted with HTML code for highlighting searched keywords.
    """
    for exploit in vulnerabilities_list:
        for keyword in keywords_list:
            file = str(exploit.port).upper()
            if file.__contains__(keyword):
                regex = re.compile(re.escape(keyword), re.IGNORECASE)
                exploit.port = regex.sub("<span class='keyword'>" + keyword + '</span>', exploit.port)
    return vulnerabilities_list
