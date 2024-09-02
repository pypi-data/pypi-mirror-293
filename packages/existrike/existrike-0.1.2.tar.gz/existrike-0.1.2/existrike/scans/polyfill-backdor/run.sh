#!/bin/bash

url=$1

echo "Running port scan on $url"
# Use o caminho completo para o script tcp.py
python3 "$(dirname "$0")/polyfill.py" -u $url -w xss.txt -s false -r "<script[^>]* src=['\"]https?://([a-zA-Z0-9-]*.)?polyfill.io[/'\"]"
