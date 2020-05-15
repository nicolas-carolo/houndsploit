$HOUNDSPLOIT_PATH = "$HOME/.HoundSploit"

$scriptFolder = (Get-Location).Path

if (-not (Test-Path $HOUNDSPLOIT_PATH)) {
    mkdir $HOUNDSPLOIT_PATH 
}

if (-not (Test-Path $HOUNDSPLOIT_PATH\exploitdb)) {
    cd $HOUNDSPLOIT_PATH
    git clone https://github.com/offensive-security/exploitdb
} else {
    cd $HOUNDSPLOIT_PATH\exploitdb
    $gitOutput = git pull
    if ($gitOutput -eq "Already up to date.") {
        Write-Host "Database already up-to-date"
    } else {
        if (-not (Test-Path $HOUNDSPLOIT_PATH\hound_db.sqlite3)) {
            rm $HOUNDSPLOIT_PATH\hound_db.sqlite3
        }
        New-Item $HOUNDSPLOIT_PATH\houndsploit_db.lock
        Write-Host "Latest version of the database downloaded"
    }
}

if (-not (Test-Path $HOUNDSPLOIT_PATH\houndsploit)) {
    git clone https://github.com/nicolas-carolo/houndsploit $HOUNDSPLOIT_PATH\houndsploit
}

cd $HOUNDSPLOIT_PATH\houndsploit
$gitOutput = git pull
if ($gitOutput -eq "Already up to date.") {
    Write-Host "HoundSploit already up-to-date"
} else {
    New-Item $HOUNDSPLOIT_PATH\houndsploit_sw.lock
    Write-Host "Latest version of HoundSploit downloaded"
    Write-Host "Run the following commands (be sure to use the Python 3 interpreter)"
    Write-Host "\tPS> pip install -r $HOUNDSPLOIT_PATH\houndsploit\requirements.txt"
    Write-Host "\tPS> cd $HOUNDSPLOIT_PATH\houndsploit"
    Write-Host "\tPS> rm $HOUNDSPLOIT_PATH\houndsploit_sw.lock"
    Write-Host "\tPS> python setup.py install"
    Write-Host "\tPS> houndsploit"
}

cd $scriptFolder