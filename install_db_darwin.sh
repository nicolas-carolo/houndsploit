#!/bin/bash
HOUNDSPLOIT_PATH="$HOME/.HoundSploit"
HOUNDSPLOIT_OLD_PATH="$HOME/HoundSploit"

if [ $(id -u) = 0 ]; then
	echo "ERROR: This script must NOT be run as 'root'"
	exit 1
fi

if ! [ $(uname) == "Darwin" ] ; then
    echo "ERROR: This installation script is only for systems running macOS"
    exit 1
fi

if ! [ -d "$HOUNDSPLOIT_PATH" ] ; then
    mkdir $HOUNDSPLOIT_PATH
fi

if ! [ -d "$HOUNDSPLOIT_PATH/exploitdb" ] ; then
    cd $HOUNDSPLOIT_PATH
    git clone https://github.com/offensive-security/exploitdb
else
    cd $HOUNDSPLOIT_PATH/exploitdb
    git_output=$(git pull)
	if [ "$git_output" == "Already up to date." ]  ; then
        echo "Database already up-to-date"
    else
        if [ -f "$HOUNDSPLOIT_PATH/hound_db.sqlite3" ] ; then
            rm $HOUNDSPLOIT_PATH/hound_db.sqlite3
        fi
        touch $HOUNDSPLOIT_PATH/houndsploit_db.lock
        echo "Latest version of the database downloaded"
    fi
fi

if ! [ -d "$HOUNDSPLOIT_PATH/houndsploit" ] ; then
    git clone https://github.com/nicolas-carolo/houndsploit $HOUNDSPLOIT_PATH/houndsploit
fi

cd $HOUNDSPLOIT_PATH/houndsploit
git_output=$(git pull)
if [ "$git_output" == "Already up to date." ]  ; then
    echo "HoundSploit already up-to-date"
else
    touch $HOUNDSPLOIT_PATH/houndsploit_sw.lock
    echo "Latest version of HoundSploit downloaded"
    echo "Run the following commands (be sure to use the Python 3 interpreter)"
    echo -e "\t$ pip install -r $HOUNDSPLOIT_PATH/houndsploit/requirements.txt"
    echo -e "\t$ cd $HOUNDSPLOIT_PATH/houndsploit"
    echo -e "\t$ rm $HOUNDSPLOIT_PATH/houndsploit_sw.lock"
    echo -e "\t$ python setup.py install"
    echo -e "\t$ houndsploit"
fi

if [ -d $HOUNDSPLOIT_OLD_PATH  ] ; then
    if [ -f "$HOUNDSPLOIT_PATH/custom_suggestions.csv" ] ; then
        cp $HOUNDSPLOIT_OLD_PATH/custom_suggestions.csv $HOUNDSPLOIT_PATH/custom_suggestions.csv
    fi
    if [ -d $HOUNDSPLOIT_OLD_PATH/houndsploit  ] && ! [ -d $HOUNDSPLOIT_OLD_PATH/hsploit  ] ; then
        rm -fr $HOUNDSPLOIT_OLD_PATH
        echo "Old HoundSploit's and hsploit's files have been removed"
    else
        rm -fr $HOUNDSPLOIT_OLD_PATH/houndsploit
        echo "Old HoundSploit's files have been removed"
    fi
fi