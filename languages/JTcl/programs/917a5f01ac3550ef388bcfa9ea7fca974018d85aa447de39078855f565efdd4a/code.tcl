proc fibonacci {n} {
    if {$n <= 1} {
        return $n
    }
    return [expr {[fibonacci [expr {$n - 1}]] + [fibonacci [expr {$n - 2}]]}]
}

for {set i 0} {$i <= 10} {incr i} {
    puts "fibonacci($i) = [fibonacci $i]"
}
