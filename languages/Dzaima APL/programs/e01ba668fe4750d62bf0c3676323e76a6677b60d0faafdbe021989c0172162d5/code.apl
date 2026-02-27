⍝ Dzaima APL: Fibonacci sequence
fib ← {⍵≤1:⍵ ⋄ (∇⍵-1)+(∇⍵-2)}
⎕←'Fibonacci numbers:'
⎕←fib¨⍳10
⎕←'Sum of first 10 Fibonacci numbers:'
⎕←+/fib¨⍳10
