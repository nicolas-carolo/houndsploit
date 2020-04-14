import csv
import sqlite3
import os


def create_db():
    init_path = os.path.expanduser("~") + "/HoundSploit"
    db_path = init_path + "/hound_db.sqlite3"
    con = sqlite3.connect(db_path)
    cur = con.cursor()

    cur.execute("CREATE TABLE searcher_exploit (id, file, description, date, author, type, platform, port);")
    exploits_path = init_path + "/exploitdb/files_exploits.csv"
    with open(exploits_path, 'r') as fin:
        dr = csv.DictReader(fin)
        to_db = [(i['id'], i['file'], i['description'], i['date'], i['author'], i['type'], i['platform'], i['port']) for i in dr]
    cur.executemany("INSERT INTO searcher_exploit (id, file, description, date, author, type, platform, port) VALUES (?, ?, ?, ?, ?, ?, ?, ?);", to_db)

    cur.execute("CREATE TABLE searcher_shellcode (id, file, description, date, author, type, platform);")
    shellcodes_path = init_path + "/exploitdb/files_shellcodes.csv"
    with open(shellcodes_path, 'r') as fin:
        dr = csv.DictReader(fin)
        to_db = [(i['id'], i['file'], i['description'], i['date'], i['author'], i['type'], i['platform']) for i in dr]
    cur.executemany("INSERT INTO searcher_shellcode (id, file, description, date, author, type, platform) VALUES (?, ?, ?, ?, ?, ?, ?);", to_db)

    cur.execute("CREATE TABLE searcher_suggestion (searched, suggestion, autoreplacement);")
    suggestions_path = init_path + "/houndsploit/csv/files_suggestions.csv"
    with open(suggestions_path, 'r') as fin:
        dr = csv.DictReader(fin)
        to_db = [(i['searched'], i['suggestion'], i['autoreplacement']) for i in dr]
    cur.executemany("INSERT INTO searcher_suggestion (searched, suggestion, autoreplacement) VALUES (?, ?, ?);", to_db)

    con.commit()
    con.close()

    try:
        f = open(os.path.expanduser("~") + "/HoundSploit/houndsploit_db.lock")
        f.close()
        os.remove(os.path.expanduser("~") + "/HoundSploit/houndsploit_db.lock") 
    except IOError:
        pass