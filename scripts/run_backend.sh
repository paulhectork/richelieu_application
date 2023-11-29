#!/usr/bin/env bash

dir=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
cd "$dir/../backend/"
if [ ! -d env ]; 
then echo "* python virtualenv called 'env' doesn't exist. run 'scripts/install_backend.sh' before. exiting..." && exit 1; 
fi;
source env/bin/activate
python main.py

