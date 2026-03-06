| fibonacci |
fibonacci := [:n |
    | a b temp |
    a := 0.
    b := 1.
    n timesRepeat: [
        temp := b.
        b := a + b.
        a := temp.
    ].
    a
].

Transcript showCr: 'Fibonacci sequence:'.
0 to: 15 do: [:i |
    Transcript showCr: 'fib(' , i printString , ') = ' , (fibonacci value: i) printString.
].
