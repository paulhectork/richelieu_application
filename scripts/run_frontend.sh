#!/usr/bin/env bash

# run the frontend
# usage: bash run_frontend.sh

dir=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
cd "$dir/../frontend"
npm install
npm run dev -- --mode backend-local
