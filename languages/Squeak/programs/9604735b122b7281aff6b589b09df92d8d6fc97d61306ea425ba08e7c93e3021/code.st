Object subclass: #Fibonacci
    instanceVariableNames: ''
    classVariableNames: ''
    poolDictionaries: ''
    category: 'Examples'

Fibonacci class >> compute: n
    "Calculate the nth Fibonacci number recursively"
    n <= 1 ifTrue: [ ^ n ].
    ^ (self compute: n - 1) + (self compute: n - 2)

Fibonacci class >> computeIterative: n
    "Calculate the nth Fibonacci number iteratively"
    | a b temp |
    a := 0.
    b := 1.
    n timesRepeat: [
        temp := a + b.
        a := b.
        b := temp
    ].
    ^ a

"Example usage:"
Fibonacci compute: 10.
Fibonacci computeIterative: 10.
