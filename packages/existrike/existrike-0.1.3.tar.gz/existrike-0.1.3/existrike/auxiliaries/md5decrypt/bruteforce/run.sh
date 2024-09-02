#!/bin/bash

hash=$1
wordlist=$2
echo "brute forcing on hash md5: $hash"
python3 "$(dirname "$0")/md5.py" -i $hash -w "$(dirname "$0")/"$2".txt"
