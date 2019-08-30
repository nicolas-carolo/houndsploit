import csv
import sqlite3
import os


def create_db():
    os.system('rm hound_db.sqlite3')

    con = sqlite3.connect("./hound_db.sqlite3")
    cur = con.cursor()

    cur.execute("CREATE TABLE searcher_exploit (id, file, description, date, author, type, platform, port);")
    with open('./csv/files_exploits.csv', 'r') as fin:
        dr = csv.DictReader(fin)
        to_db = [(i['id'], i['file'], i['description'], i['date'], i['author'], i['type'], i['platform'], i['port']) for i in dr]
    cur.executemany("INSERT INTO searcher_exploit (id, file, description, date, author, type, platform, port) VALUES (?, ?, ?, ?, ?, ?, ?, ?);", to_db)

    cur.execute("CREATE TABLE searcher_shellcode (id, file, description, date, author, type, platform);")
    with open('./csv/files_shellcodes.csv', 'r') as fin:
        dr = csv.DictReader(fin)
        to_db = [(i['id'], i['file'], i['description'], i['date'], i['author'], i['type'], i['platform']) for i in dr]
    cur.executemany("INSERT INTO searcher_shellcode (id, file, description, date, author, type, platform) VALUES (?, ?, ?, ?, ?, ?, ?);", to_db)

    con.commit()
    con.close()


if __name__ == "__main__":
    main()