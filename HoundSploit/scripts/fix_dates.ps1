$HOUNDSPLOIT_PATH = "$HOME/.HoundSploit"

$scriptFolder = (Get-Location).Path

cd $HOUNDSPLOIT_PATH

Copy-Item -Recurse .\exploitdb\ fixed_exploitdb
cd fixed_exploitdb
git checkout 23acd8a13b7a871e735016897c7a9e7b0ac33448

cd $scriptFolder