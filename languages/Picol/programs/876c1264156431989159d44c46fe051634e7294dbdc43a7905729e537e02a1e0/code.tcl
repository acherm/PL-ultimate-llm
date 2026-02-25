proc fib {n} {
    if {<= $n 1} {
        return $n
    } {
        return [+ [fib [- $n 1]] [fib [- $n 2]]]
    }
}

set i 0
while {< $i 10} {
    puts [fib $i]
    set i [+ $i 1]
}
