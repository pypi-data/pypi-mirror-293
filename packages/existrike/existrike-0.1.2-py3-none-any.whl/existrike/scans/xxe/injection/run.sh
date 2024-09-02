#!/bin/bash

url=$1

echo "Running port scan on $url"
# Use o caminho completo para o script tcp.py
python3 "$(dirname "$0")/xxe.py" -u $url -w xss.txt -s false -r "root:.+:0:0:root:/root:/bin/bash"
