#!/bin/bash

url=$1
path=$2

echo "testing payloads to bypass 403 in $url"
# Use o caminho completo para o script tcp.py
python3 "$(dirname "$0")/403.py" $url $path