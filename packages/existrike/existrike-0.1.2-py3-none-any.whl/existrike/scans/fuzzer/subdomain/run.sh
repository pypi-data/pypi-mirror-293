#!/bin/bash

url=$1
output_file="$(dirname "$0")/../../../output/subdomain.txt"

echo "Running port scan on $url"
# Use o caminho completo para o script tcp.py
python3 "$(dirname "$0")/fuzz.py" -d $url -w "$(dirname "$0")/wordlist.txt" -c -s "$output_file"
echo "output saved on output/subdomain.txt"
