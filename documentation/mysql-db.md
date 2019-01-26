# How create a MySQL DB for HoundSploit

## Download and configure MySQL

1. Download and install MySQL for your platform. I suggest you also to install _MySQLWorkbench_ if you want a GUI for manage the DB.
2. Download and install _mysqlclient_ (if you have a Mac running macOS read the dedicated section in this page).

### Download and install _mysqlclient_ on macOS
1. Get _Homebrew_ if you haven't installed it yet.
2. Open the Terminal and execute `brew install mysql-connector-c`.
3. Then find the location of `mysql_config` running `which mysql_config`.
4. Open `mysql_config` file and change the following lines
    ```
    # Create options 
    libs="-L$pkglibdir"
    libs="$libs -l "
    ```

    in

    ```
    # Create options 
    libs="-L$pkglibdir"
    libs="$libs -lmysqlclient -lssl -lcrypto"
    ```
5. Run `brew info openssl`.
6. Now you can install _mysqlclient_: `pip install mysqlclient.`

## Create HOUNDSPLOIT db connection and the relative tablese

### Starting from .csv files
1. Get `files_exploits.csv` and `files_shellcodes.csv` from the [Exploit-DB repository on GitHub](https://github.com/offensive-security/exploitdb).
2. Now you have to create a SQL script for each file. For examples I have used the online converter available on this link:[http://convertcsv.com/csv-to-sql.htm](http://convertcsv.com/csv-to-sql.htm). Creating the two scripts remember that the exploits table have to be named as `searcher_exploit`, while the shellcodes table as `searcher_shellcode`. After making the convertion, download and save the two SQL scripts you have just created. I have saved them respectively as `files_exploits.sql` and `files_shellcodes.sql`. 

### Starting from SQL scripts

**N.B.:** In this guide I am going to describe the procedure using _MySQLWorkbench_.

1. Open _MySQLWorkbench_.
2. Create a new connection named `HOUNDSPLOIT` and select `utf32 - default collation` for the `Default Collation` configuration parameter. This choice is necessary because some vulnerabilities' authors have names that contain a set of characters that belong to a great variety of alphabets.
3. Create `searcher_exploit` and `searcher_shellcode` tables executing `files_exploits.sql` and `files_shellcodes.sql` scripts.
4. Create a new db user:

    user: `hound-user`

    password: `hound-password`

    and remember to assign him the privilege to make `SELECT` operations.
    If you want to user other parameters for the connection to the database, such as a different user or a different password or a different connection name, you have to edit the configurations parameters of the constant `DATABASES` in `HoundSploit/settings.py`.
5. Now you can run HoundSploit and test if it works fine!


