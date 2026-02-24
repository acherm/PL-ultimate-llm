⍝ Fibonacci sequence in Dyalog APL
⍝ Recursive dfn (direct function) definition
fib←{⍵≤1:⍵ ⋄ (∇⍵-1)+∇⍵-2}

⍝ Display first 11 Fibonacci numbers (indices 0 to 10)
⎕←fib¨⍳11
