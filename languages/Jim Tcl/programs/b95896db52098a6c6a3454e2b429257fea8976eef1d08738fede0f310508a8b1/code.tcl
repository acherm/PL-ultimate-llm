#!/usr/bin/env jimsh

# Fibonacci sequence calculator using memoization
proc fib {n} {
    global fibCache
    if {$n <= 1} {
        return $n
    }
    if {[info exists fibCache($n)]} {
        return $fibCache($n)
    }
    set fibCache($n) [expr {[fib [expr {$n - 1}]] + [fib [expr {$n - 2}]]}]
    return $fibCache($n)
}

# Calculate and display Fibonacci numbers
puts "Fibonacci sequence:"
for {set i 0} {$i < 15} {incr i} {
    puts "F($i) = [fib $i]"
}
