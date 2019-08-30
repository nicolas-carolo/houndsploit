import zipfile
import requests
import re
import os

from searcher.engine.csv2sqlite import create_db


def is_update_available(repo, filename_last_commit):
    try:
        info_request = requests.get('https://api.github.com/repos/{0}/commits?per_page=1'.format(repo))
        commit = info_request.json()[0]["commit"]
        regex = re.search(r'\'message\': (\'|\")(?P<last_git_commit>.*)(\'|\")\, \'tree\'', str(commit))
        try:
            last_git_commit = regex.group('last_git_commit')
            try:
                with open(filename_last_commit, 'r') as f:
                    content = f.readlines()
                    last_local_commit = ''.join(content)
                if str(last_local_commit) == str(last_git_commit):
                    return False
                else:
                    return True
            except FileNotFoundError:
                return True
        except AttributeError:
            print("error")
            return False
    except KeyError:
        return False


def download_update():
    os.system('wget https://github.com/nicolas-carolo/HoundSploitBash/archive/master.zip -O ~/HoundSploitBash.zip')
    print('The zip archive \'HoundSploitBash.zip\' has been saved in your home directory.')
    print('Download completed!')
    print('Remember to run setup.py before use HoundSploit again')
    exit(0)


def install_exploitdb_update():
    try:
        info_request = requests.get('https://api.github.com/repos/{0}/commits?per_page=1'.format("offensive-security/exploitdb"))
        commit = info_request.json()[0]["commit"]
        regex = re.search(r'\'message\': (\'|\")(?P<last_git_commit>.*)(\'|\")\, \'tree\'', str(commit))
        last_git_commit = regex.group('last_git_commit')
        os.system('rm -fr ./searcher/vulnerabilities/*')
        if os.path.isfile("./hound_db.sqlite3"):
            os.system('rm ./hound_db.sqlite3')
        if os.path.isdir("exploitdb_temp"):
            os.system('rm -fr exploitdb_temp')
        if not os.path.isdir("csv"):
            os.system('mkdir csv')
        if not os.path.isdir("./searcher/vulnerabilities"):
            os.system('mkdir ./searcher/vulnerabilities')
        os.system('wget https://github.com/offensive-security/exploitdb/archive/master.zip -O ./exploitdb.zip')
        os.system('mkdir exploitdb_temp')
        with zipfile.ZipFile("./exploitdb.zip", 'r') as zip_ref:
            zip_ref.extractall("exploitdb_temp")
        os.system('mv ./exploitdb_temp/exploitdb-master/exploits ./searcher/vulnerabilities/exploits')
        os.system('mv ./exploitdb_temp/exploitdb-master/shellcodes ./searcher/vulnerabilities/shellcodes')
        os.system('mv ./exploitdb_temp/exploitdb-master/files_exploits.csv ./csv')
        os.system('mv ./exploitdb_temp/exploitdb-master/files_shellcodes.csv ./csv')
        create_db()
        os.system('rm -fr exploitdb_temp')
        os.system('rm exploitdb.zip')
        f = open("./searcher/etc/latest_exploitdb_commit.txt", "w")
        f.write(last_git_commit)
        f.close()
        print('The latest version of the database has been download successfully!')
    except AttributeError:
        print('Error in updating the database')


def get_latest_db_update_date():
    try:
        with open("./searcher/etc/latest_exploitdb_commit.txt", 'r') as f:
            content = f.readlines()
            latest_local_commit = ''.join(content)
        regex = re.search(r'DB: (?P<date>\d\d\d\d\-\d\d\-\d\d)', str(latest_local_commit))
        try:
            latest_db_update_date = regex.group('date')
            return latest_db_update_date
        except AttributeError:
            return ""
    except FileNotFoundError:
        return ""

