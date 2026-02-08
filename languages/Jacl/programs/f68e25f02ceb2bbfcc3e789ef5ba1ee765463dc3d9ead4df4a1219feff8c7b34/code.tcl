# Fibonacci sequence calculator in Jacl
proc fibonacci {n} {
    if {$n <= 1} {
        return $n
    }
    set a 0
    set b 1
    for {set i 2} {$i <= $n} {incr i} {
        set temp [expr {$a + $b}]
        set a $b
        set b $temp
    }
    return $b
}

# Calculate and print first 10 Fibonacci numbers
puts "First 10 Fibonacci numbers:"
for {set i 0} {$i < 10} {incr i} {
    puts "F($i) = [fibonacci $i]"
}
