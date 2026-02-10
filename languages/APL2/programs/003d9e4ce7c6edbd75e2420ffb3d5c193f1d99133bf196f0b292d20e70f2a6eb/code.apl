⍝ Sieve of Eratosthenes
⍝ Returns all primes up to N
Primes←{
    N←⍵
    P←2=+⌿0=∘.|⍨⍳N
    P/⍳N
}

⍝ Example: Primes 30
⍝ Result: 2 3 5 7 11 13 17 19 23 29