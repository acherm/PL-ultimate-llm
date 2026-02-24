#!/usr/bin/ksh
# Fibonacci sequence
integer i a=0 b=1 c
for ((i=0; i<20; i++)) do
    print $a
    c=a+b; a=b; b=c
done
