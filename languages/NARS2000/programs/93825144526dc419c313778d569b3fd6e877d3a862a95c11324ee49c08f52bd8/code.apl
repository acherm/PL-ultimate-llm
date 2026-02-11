⍝ Sieve of Eratosthenes - finds all prime numbers up to N
∇ result ← Sieve N
  ⍝ Create a boolean vector where 1 means prime
  result ← (N⍴1)
  result[1] ← 0
  ⍝ Mark multiples of each number as composite
  :For i :In 2..⌊N*0.5
    :If result[i]
      result[i×⍳⌊N÷i] ← 0
    :EndIf
  :EndFor
  ⍝ Return the indices where result is 1 (the primes)
  result ← result/⍳N
∇