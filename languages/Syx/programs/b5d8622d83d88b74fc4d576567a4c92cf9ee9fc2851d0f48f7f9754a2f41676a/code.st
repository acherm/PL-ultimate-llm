"Fibonacci sequence calculator using recursion and memoization"

Object subclass: #FibonacciCalculator
    instanceVariableNames: 'cache'
    classVariableNames: ''
    poolDictionaries: ''
    category: 'Mathematics'.

FibonacciCalculator>>initialize
    super initialize.
    cache := Dictionary new.
    cache at: 0 put: 0.
    cache at: 1 put: 1.

FibonacciCalculator>>fibonacci: n
    "Calculate the nth Fibonacci number using memoization"
    (cache includesKey: n) ifTrue: [
        ^cache at: n
    ].

    | result |
    result := (self fibonacci: n - 1) + (self fibonacci: n - 2).
    cache at: n put: result.
    ^result.

FibonacciCalculator>>printFirst: count
    "Print the first count Fibonacci numbers"
    1 to: count do: [:i |
        Transcript show: 'F(', i printString, ') = ', (self fibonacci: i) printString; cr
    ].

"Usage example"
| calculator |
calculator := FibonacciCalculator new.
calculator printFirst: 10.
