-- IHaskell: Sieve of Eratosthenes
-- In IHaskell, top-level expressions are evaluated and their results displayed

primes :: [Int]
primes = sieve [2..]
  where
    sieve (p:xs) = p : sieve [x | x <- xs, x `mod` p /= 0]
    sieve [] = []

-- Display first 20 primes (IHaskell auto-displays top-level expressions)
take 20 primes
