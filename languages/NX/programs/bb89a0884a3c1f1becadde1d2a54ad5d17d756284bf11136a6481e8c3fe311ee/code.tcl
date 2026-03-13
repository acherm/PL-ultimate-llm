package require nx

# A simple Stack implementation in NX (Next Scripting Language)
nx::Class create Stack {
    :variable items {}

    :public method push {item} {
        lappend :items $item
    }

    :public method pop {} {
        if {[llength ${:items}] == 0} {
            error "Stack underflow"
        }
        set top [lindex ${:items} end]
        set :items [lrange ${:items} 0 end-1]
        return $top
    }

    :public method peek {} {
        if {[llength ${:items}] == 0} {
            error "Stack is empty"
        }
        return [lindex ${:items} end]
    }

    :public method size {} {
        return [llength ${:items}]
    }

    :public method isEmpty {} {
        return [expr {[llength ${:items}] == 0}]
    }
}

# Create a stack instance and use it
Stack create s

s push 10
s push 20
s push 30

puts "Stack size: [s size]"
puts "Top element: [s peek]"
puts "Popped: [s pop]"
puts "Stack size after pop: [s size]"
puts "Is empty: [s isEmpty]"
