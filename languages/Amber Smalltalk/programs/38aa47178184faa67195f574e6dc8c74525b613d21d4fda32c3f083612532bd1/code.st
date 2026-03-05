| primes sieve |
sieve := (2 to: 50) asOrderedCollection.
primes := OrderedCollection new.
[sieve isEmpty] whileFalse: [
    | p |
    p := sieve first.
    primes add: p.
    sieve := sieve select: [:n | (n \\ p) ~= 0]].
Transcript show: 'Primes up to 50: ', primes printString; nl.
