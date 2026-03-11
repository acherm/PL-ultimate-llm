#!/usr/bin/env ksh

function fib {
    integer n=$1
    if (( n < 2 )); then
        print $n
    else
        print $(( $(fib $((n-1))) + $(fib $((n-2))) ))
    fi
}

integer i
for (( i=0; i<=10; i++ )); do
    print "F($i) = $(fib $i)"
done
