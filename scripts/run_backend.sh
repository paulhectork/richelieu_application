#!/usr/bin/env bash

# launch the backend (needs to have a virtual environment named `env` in the `backend/` dir
# usage: bash run_backend.sh

dir=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
cd "$dir/../backend/"
if [ ! -d env ]; 
then echo "* python virtualenv called 'env' in 'backend/' doesn't exist. run 'python3 -m venv env' before. exiting..." && exit 1;
fi;
source env/bin/activate
pip install -r ./requirements.txt
python main.py -m dev

