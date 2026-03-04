Object subclass: #FibonacciCalc
    instanceVariableNames: ''
    classVariableNames: ''
    poolDictionaries: ''
    category: 'Examples'.

FibonacciCalc class >> fib: n [
    n <= 1 ifTrue: [ ^n ].
    ^(self fib: n - 1) + (self fib: n - 2)
]

| result |
0 to: 10 do: [ :i |
    result := FibonacciCalc fib: i.
    Transcript showCr: 'fib(' , i printString , ') = ' , result printString ].