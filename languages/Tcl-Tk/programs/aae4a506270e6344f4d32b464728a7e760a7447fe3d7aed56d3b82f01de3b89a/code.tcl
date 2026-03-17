proc fibonacci {n} {
    if {$n <= 1} {
        return $n
    }
    set a 0
    set b 1
    for {set i 2} {$i <= $n} {incr i} {
        set c [expr {$a + $b}]
        set a $b
        set b $c
    }
    return $b
}

for {set i 0} {$i <= 10} {incr i} {
    puts "fib($i) = [fibonacci $i]"
}
