#!/bin/sh
# File counter script

count_files() {
    dir="$1"
    if [ -d "$dir" ]; then
        count=0
        for file in "$dir"/*; do
            if [ -f "$file" ]; then
                count=$((count + 1))
            fi
        done
        echo "$count"
    else
        echo "0"
    fi
}

if [ $# -eq 0 ]; then
    echo "Usage: $0 <directory>"
    exit 1
fi

result=$(count_files "$1")
echo "Number of files in $1: $result"