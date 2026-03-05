Object subclass: #FibCalculator
    instanceVariableNames: ''
    classVariableNames: ''
    poolDictionaries: ''
    category: 'Examples'!

!FibCalculator class methodsFor: 'computing'!
fibonacci: n
    n <= 1 ifTrue: [^n].
    ^(self fibonacci: n - 1) + (self fibonacci: n - 2)
! !

Transcript showCr: 'Fibonacci numbers:'.
0 to: 10 do: [:i |
    Transcript showCr: 'fib(' , i printString , ') = ' ,
        (FibCalculator fibonacci: i) printString
].
