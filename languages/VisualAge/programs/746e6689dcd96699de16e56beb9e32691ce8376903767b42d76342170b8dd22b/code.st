| fibonacci |
fibonacci := [:n |
    n <= 1
        ifTrue: [n]
        ifFalse: [(fibonacci value: n - 1) + (fibonacci value: n - 2)]
].

Transcript showCr: 'Fibonacci sequence:'.
0 to: 10 do: [:i |
    Transcript
        show: 'fib(';
        show: i printString;
        show: ') = ';
        showCr: (fibonacci value: i) printString.
].
