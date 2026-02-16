Transcript showCR: 'Fibonacci numbers:'.
1 to: 15 do: [:i |
    | fib |
    fib := [:n |
        n <= 1
            ifTrue: [n]
            ifFalse: [(fib value: n - 1) + (fib value: n - 2)]
    ].
    Transcript show: 'F(', i printString, ') = '.
    Transcript showCR: (fib value: i) printString
]
