#!/bin/bash

url=$1

echo "Running port scan on $url"
# Use o caminho completo para o script tcp.py
python3 "$(dirname "$0")/lfi.py" -u $url -w lfi.txt -s false -r "root:x:"
