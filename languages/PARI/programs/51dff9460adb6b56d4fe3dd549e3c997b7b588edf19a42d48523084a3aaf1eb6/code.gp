/* Sieve of Eratosthenes in PARI/GP */

sieve(n) = {
    my(v = vectorsmall(n, i, 1));
    v[1] = 0;
    for(k = 2, sqrtint(n),
        if(v[k],
            forstep(j = k^2, n, k,
                v[j] = 0
            )
        )
    );
    select(i -> v[i], [1..n])
}

\\ Print all primes up to 50
print(sieve(50))
