# NimScript example: simple task runner and utilities
# NimScript is the scripting subset of the Nim programming language

proc isPrime(n: int): bool =
  if n < 2: return false
  if n == 2: return true
  if n mod 2 == 0: return false
  var i = 3
  while i * i <= n:
    if n mod i == 0: return false
    i += 2
  true

proc firstNPrimes(n: int): seq[int] =
  result = @[]
  var candidate = 2
  while result.len < n:
    if isPrime(candidate):
      result.add(candidate)
    inc candidate

let primes = firstNPrimes(10)
echo "First 10 primes: ", primes
