#!/bin/csh
# Fibonacci sequence in Hamilton C shell
# Demonstrates variables, arithmetic, loops, and output

set n = 10
set a = 0
set b = 1

echo "First $n Fibonacci numbers:"

set i = 1
while ($i <= $n)
    echo -n "$a "
    set temp = `expr $a + $b`
    set a = $b
    set b = $temp
    @ i++
end
echo ""
