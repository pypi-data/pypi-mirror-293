#!/bin/bash

user=$1
output_file="$(dirname "$0")/../../../../output/wordlist.txt"

echo "Running wordlist gen to $user"
python3 "$(dirname "$0")/admin.py" -d $user -o "$output_file" -i

echo "Wordlist has been generated and saved to output/wordlist.txt"
