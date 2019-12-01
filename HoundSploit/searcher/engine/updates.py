import zipfile
import requests
import re
import os
import sys

from HoundSploit.searcher.engine.csv2sqlite import create_db


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
        init_path = os.path.split(sys.executable)[0]
        info_request = requests.get('https://api.github.com/repos/{0}/commits?per_page=1'.format("offensive-security/exploitdb"))
        commit = info_request.json()[0]["commit"]
        regex = re.search(r'\'message\': (\'|\")(?P<latest_git_commit>.*)(\'|\")\, \'tree\'', str(commit))
        latest_git_commit = regex.group('latest_git_commit')
        vulnerabilities_path = init_path + "/HoundSploit/vulnerabilities"
        if os.path.isdir(vulnerabilities_path):
            os.system('rm -fr ' + vulnerabilities_path)
        db_path = init_path + "/HoundSploit/hound_db.sqlite3"
        if os.path.isfile(db_path):
            os.system('rm ' + db_path)
        csv_path = init_path + "/HoundSploit/csv"
        if not os.path.isdir(csv_path):
            os.system('mkdir ' + csv_path)
        os.system('mkdir ' + vulnerabilities_path)
        zip_path = init_path + "/exploitdb.zip"
        os.system('wget https://github.com/offensive-security/exploitdb/archive/master.zip -O ' + zip_path)
        temp_path = init_path + "/exploitdb_temp"
        os.system('mkdir ' + temp_path)
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(temp_path)
        os.system('mv ' + temp_path + '/exploitdb-master/exploits ' + vulnerabilities_path + '/exploits')
        os.system('mv ' + temp_path + '/exploitdb-master/shellcodes ' + vulnerabilities_path + '/shellcodes')
        os.system('mv ' + temp_path + '/exploitdb-master/files_exploits.csv ' + csv_path)
        os.system('mv ' + temp_path + '/exploitdb-master/files_shellcodes.csv ' + csv_path)
        create_db(init_path)
        os.system('rm -fr ' + temp_path)
        os.system('rm ' + zip_path)
        etc_path = init_path + "/HoundSploit/etc"
        if not os.path.isdir(etc_path):
            os.system('mkdir ' + etc_path)
        latest_db_update_path = etc_path + "/latest_exploitdb_commit.txt"
        f = open(latest_db_update_path, "w")
        f.write(latest_git_commit)
        f.close()
        print('The latest version of the database has been downloaded successfully!')
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

