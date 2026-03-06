/ Fibonacci sequence in ngn/k
/ Generates first n Fibonacci numbers using scan adverb

fib:{x{x,+/-2#x}/0 1}
`0:$'fib 10
