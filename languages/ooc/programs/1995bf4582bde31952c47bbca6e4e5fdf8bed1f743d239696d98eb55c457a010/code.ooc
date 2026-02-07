// Hello World in ooc
import os/Time

main: func {
    "Hello, World!" println()

    // Simple fibonacci function
    for (i in 0..10) {
        "fib(%d) = %d" printfln(i, fib(i))
    }
}

fib: func (n: Int) -> Int {
    if (n <= 1) return n
    return fib(n - 1) + fib(n - 2)
}
