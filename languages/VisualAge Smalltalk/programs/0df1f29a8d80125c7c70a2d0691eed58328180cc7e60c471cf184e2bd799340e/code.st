| fib |
fib := [:n |
    n <= 1
        ifTrue: [n]
        ifFalse: [(fib value: n - 1) + (fib value: n - 2)]].

0 to: 15 do: [:i |
    Transcript showCr: (fib value: i) printString].
