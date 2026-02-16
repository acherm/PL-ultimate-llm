⍝ APLX Example: Compute factorial using recursion
∇ result ← Factorial n
  →(n≤1)/L1
  result ← n × Factorial n-1
  →0
L1: result ← 1
∇

⍝ Test with factorial of 10
Factorial 10
