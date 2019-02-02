import os
import requests
import re


def is_update_available():
    try:
        repo = 'nicolas-carolo/HoundSploit'
        info_request = requests.get('https://api.github.com/repos/{0}/commits?per_page=1'.format(repo))
        commit = info_request.json()[0]["commit"]
        regex = re.search(r'\'message\': \'(?P<last_git_commit>[^\']*)\'', str(commit))
        try:
            last_git_commit = regex.group('last_git_commit')
            pwd = os.path.dirname(__file__)
            regex = re.search(r'(?P<base_dir>.+)/engine', str(pwd))
            path = regex.group('base_dir') + '/static/etc/last_commit.txt'
            try:
                with open(path, 'r') as f:
                    content = f.readlines()
                    last_local_commit = ''.join(content)
                # print(last_local_commit)
                if str(last_local_commit) == str(last_git_commit):
                    return False
                else:
                    return True
            except FileNotFoundError:
                return True
        except AttributeError:
            return False
    except KeyError:
        return False
