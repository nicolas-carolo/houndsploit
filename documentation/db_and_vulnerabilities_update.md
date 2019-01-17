# How to convert `files_exploits.csv` and 'files_shellcodes.csv' into a sqlite3 db valid for HoundSploit

## Get the CSV files

If you are using Linux, probably, you have installed SearchSploit in `/opt`. In this case you can find `file_exploits.csv` in `/opt/exploitdb/`.
If you are using macOS, you can find the same file in `exploitdb/2018-08-10/share/exploit-database/`. I have found this path using `$ brew list exploitdb`
You can also get these files from [Exploit-DB repository on GitHub](https://github.com/offensive-security/exploitdb)

## Installation of sqlite3 (if you haven't installed it yet)

Install sqlite3:

`$ sudo apt-get install sqlite3`

## Creation of the DB

Create a sqlite3 db:

`$ sqlite3 db.sqlite3`

Then, in sqlite3:

`sqlite> .mode csv`

Convert the CSV files into tables of _db.sqlite3_ file:

`sqlite> .import files_exploits.csv searcher_exploit`

`sqlite> .import files_shellcodes.csv searcher_shellcode`

Then remeber to save the `db.sqlite3` file in the `HoundSploit/db.sqlite3` path.


### Some useful sqlite commands:

For viewing tables of our sqlite3 db:

`sqlite> .tables`

For counting exploits that there are in our db:

`sqlite> select count(*) from exploits`

For closing sqlite3:

`sqlite> .quit`

# Create initial Django migration for the existing DB schema

Only if `db.sqlite3` contains `django_migrations` table:

`$ sqlite3 db.sqlie3`

`sqlite> delete from django_migrations;`

Else run only these commands:

`$ rm -rf searcher/migrations/`

`$ python manage.py migrate --fake`

`$ python manage.py makemigrations searcher`

`$ python manage.py migrate --fake-initial`

The last command may not work properly. In this case do not worry and run HoundSploit for testing that allit works correctly.

# Update the repository containing the vulnerabilities files

Copy the `exploits` and the `shellcodes` folders into `HoundSploit/searcher/static/vulnerabilities` directory.

