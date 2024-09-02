#!/bin/bash

url=$1

echo "Running port scan on $url"
# Use o caminho completo para o script tcp.py
python3 "$(dirname "$0")/ssti.py" -u $url -w ssti.txt -s false -r "64"
