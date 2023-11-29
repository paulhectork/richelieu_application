#!/usr/bin/env bash

dir=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
cd "$dir/../frontend/"
npm install
npm run dev
