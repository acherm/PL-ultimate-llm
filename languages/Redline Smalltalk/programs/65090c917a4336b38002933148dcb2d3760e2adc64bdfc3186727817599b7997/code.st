Object subclass: #Fibonacci
    instanceVariableNames: ''
    classVariableNames: ''
    poolDictionaries: ''
    category: 'Example'.

Fibonacci class >> fib: n [
    ^n <= 1
        ifTrue: [n]
        ifFalse: [(self fib: n - 1) + (self fib: n - 2)]
].

1 to: 10 do: [:i |
    Transcript showCr: 'fib(', i printString, ') = ', (Fibonacci fib: i) printString].
