# HoundSploit

**HoundSploit** is an advanced search engine for Exploit-DB developed in
Python using Django Web Framework, born with the aim of showing the user
the most accurate search results.


## Features

* Effective version number filtering
* Advanced filtering
* Search suggestions with customization
* Syntax highlighting of the source code of exploits or shellcodes
* Downloading of the source code of exploits or shellcodes
* Highlighting of searched words in search results
* Automatic check for updates


### Effective version number filtering examples
#### Example I

```
nicolas@carolo:~$ searchsploit WordPress 2.0.2
WordPress 2.0.2- 'cache' Remote Shell Injection
WordPress Plugin Crawl Rate Tracker 2.0.2 - SQL Inject
WordPress Plugin Sodahead Polls 2.0.2 - Multiple Cross
```

**HoundSploit**: `WordPress 2.0.2`

10 exploits and 0 shellcodes found for "WordPress 2.0.2"

* WORDPRESS 1.5.1.1 < 2.2.2 - Multiple Vulnerabilities
* WORDPRESS < 4.0.1 - Denial of Service
* ...


#### Example II

```
nicolas@carolo:~$ searchsploit Linux Kernel 4.2.3
Exploits: No Result
Shellcodes: No Result
Papers: No Result
```

**HoundSploit**: `Linux Kernel 4.2.3`

14 exploits and 0 shellcodes found for "linux kernel 4.2.3"

* LINUX KERNEL 3.11 < 4.8 0 - 'SO_SNDBUFFORCE' / 'SO_RCVBUFFORCE' Local
Privilege Escalation
* LINUX KERNEL < 4.10.13 - 'keyctl_set_reqkey_keyring' Local Denial of 
Service
* ...


### Advanced filtering

Using advanced search you can use the following filters for filtering search
results:
* Search operator: `AND` or `OR`
* Author
* Type
* Platform
* Port
* Date interval


### Search suggestion

You can choose to show a particular suggestion for a given searched string.
For each case you can also decide to use automatic replacement or not.
It is possible to add new suggestions and delete the existing suggestions


## Documentation
[Here](https://github.com/nicolas-carolo/HoundSploit/tree/master/documentation)
you can read the software documentation.


## Updates
The database of exploits and shellcodes will be weekly updated.


