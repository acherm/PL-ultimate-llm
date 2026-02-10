#!/usr/bin/env yash
# Fibonacci sequence generator in Yash

fib() {
    typeset n=$1 a=0 b=1 temp
    if [ "$n" -le 0 ]; then
        return
    fi
    printf '%d' "$a"
    if [ "$n" -eq 1 ]; then
        printf '
'
        return
    fi
    printf ' %d' "$b"
    n=$((n - 2))
    while [ "$n" -gt 0 ]; do
        temp=$((a + b))
        a=$b
        b=$temp
        printf ' %d' "$temp"
        n=$((n - 1))
    done
    printf '
'
}

# Generate first 10 Fibonacci numbers
fib 10
