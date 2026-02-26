set a 0
puts "a is $a"
proc foo {} {
    set a 10
    puts "in foo, a is $a"
}
foo
puts "a is $a"
