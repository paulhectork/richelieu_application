#!/usr/bin/env bash

# get full dir no matter where the script is launched from / what the pwd is
# see https://stackoverflow.com/questions/59895/how-do-i-get-the-directory-where-a-bash-script-is-located-from-within-the-script
dir=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
cd "$dir/../backend/"
echo -e "* getting python env and dependencies\n"
if [ ! -d env ]; then python3 -m venv env; fi;
source env/bin/activate
pip install -r requirements.txt
echo -e "\n*************************************\n"
echo -e "* launching the backend app\n"
python main.py
