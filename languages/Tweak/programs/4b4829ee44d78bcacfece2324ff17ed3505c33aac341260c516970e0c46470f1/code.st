"Fibonacci sequence in Tweak/Squeak Smalltalk"
| a b temp |
Transcript showCr: 'Fibonacci Sequence:'.
a := 0.
b := 1.
0 to: 10 do: [:i |
    Transcript showCr: 'fib(' , i printString , ') = ' , a printString.
    temp := a + b.
    a := b.
    b := temp.
].
