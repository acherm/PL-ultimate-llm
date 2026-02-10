Object subclass: #FactorialCalculator
    instanceVariableNames: ''
    classVariableNames: ''
    poolDictionaries: ''
    category: 'Examples'!

!FactorialCalculator class methodsFor: 'computing' stamp: 'test 1/1/2026 12:00'!
factorial: n
    "Compute the factorial of n"
    ^ n <= 1
        ifTrue: [1]
        ifFalse: [n * (self factorial: n - 1)]! !

"Example usage"
Transcript show: 'Factorial of 5 is: '.
Transcript show: (FactorialCalculator factorial: 5) printString.
Transcript cr.
