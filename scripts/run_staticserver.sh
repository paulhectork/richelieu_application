#!/usr/bin/env bash

# launch the local static file server. needs to have a python virtualenv named `env` in `staticserver/`
# usage: bash run_staticserver.sh

dir=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
cd "$dir/../staticserver/"
if [ ! -d env ]; 
then echo "* python virtualenv called 'env' in 'staticserver/' doesn't exist. run 'python3 -m venv env' before. exiting..." && exit 1;
fi;
source env/bin/activate
pip install -r ./requirements.txt
python main.py

