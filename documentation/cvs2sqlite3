# How convert `file_exploits.csv` into a sqlite3 db

Install sqlite3:

`$ sudo apt-get install sqlite3`

Create a sqlite3 db:

`$ sqlite3 db.sqlite3`

Then, in sqlite3:

`sqlite> .mode csv`

Convert the CSV file into a sqlite3 db, specifying the name of the table:

`sqlite> .import files_exploits.csv exploits`


## Some useful commands:

For viewing tables of our sqlite3 db:

`sqlite> .tables`

For counting exploits that there are in our db:

`sqlite> select count(*) from exploits`

For closing sqlite3:

`sqlite> .quit`
