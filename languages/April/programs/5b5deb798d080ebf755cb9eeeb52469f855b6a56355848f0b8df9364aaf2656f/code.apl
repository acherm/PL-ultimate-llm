⍝ Fibonacci sequence generator
fib ← {⍵<2:⍵ ⋄ (∇ ⍵-1)+∇ ⍵-2}
⍝ Generate first 10 Fibonacci numbers
fib ¨ ⍳10
