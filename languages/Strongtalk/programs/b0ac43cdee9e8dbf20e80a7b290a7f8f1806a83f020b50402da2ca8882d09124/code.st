"Fibonacci sequence calculator with type annotations"

fibonacci: n <Integer> ^ <Integer>
  "Calculate the nth Fibonacci number"
  n <= 1
    ifTrue: [^n]
    ifFalse: [^(self fibonacci: n - 1) + (self fibonacci: n - 2)].

"Calculate and display first 10 Fibonacci numbers"
1 to: 10 do: [:i |
  Transcript show: 'F(', i printString, ') = ', (self fibonacci: i) printString; cr
].
