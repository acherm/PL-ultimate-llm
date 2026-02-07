fib: func [n] [
    either n < 2 [
        n
    ][
        add fib n - 1 fib n - 2
    ]
]

loop 15 [i] [
    print fib i
]