#!/bin/mksh
# Fibonacci sequence generator
# https://github.com/MirOS/mksh/blob/master/examples/fibonacci.sh

function fibonacci {
    typeset -i n=$1
    typeset -i a=0 b=1 c

    if (( n <= 0 )); then
        return
    elif (( n == 1 )); then
        print $a
    else
        print -n "$a "
        while (( n-- > 1 )); do
            print -n "$b "
            c=$((a + b))
            a=$b
            b=$c
        done
        print
    fi
}

# Generate first 15 Fibonacci numbers
fibonacci 15