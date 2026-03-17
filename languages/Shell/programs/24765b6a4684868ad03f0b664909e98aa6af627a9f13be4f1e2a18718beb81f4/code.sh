#!/bin/sh
# Fibonacci sequence - iterative implementation

fibonacci() {
    n=$1
    if [ "$n" -le 0 ]; then
        echo 0
        return
    fi
    a=0
    b=1
    i=1
    while [ "$i" -lt "$n" ]; do
        c=$((a + b))
        a=$b
        b=$c
        i=$((i + 1))
    done
    echo $b
}

echo "Fibonacci sequence (first 10 terms):"
i=0
while [ "$i" -lt 10 ]; do
    result=$(fibonacci $i)
    printf "F(%d) = %d\n" "$i" "$result"
    i=$((i + 1))
done
