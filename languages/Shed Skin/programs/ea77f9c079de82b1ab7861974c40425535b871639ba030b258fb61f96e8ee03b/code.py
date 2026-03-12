def sieve(limit):
    is_prime = [True] * (limit + 1)
    is_prime[0] = False
    is_prime[1] = False
    i = 2
    while i * i <= limit:
        if is_prime[i]:
            j = i * i
            while j <= limit:
                is_prime[j] = False
                j += i
        i += 1
    result = []
    for k in range(limit + 1):
        if is_prime[k]:
            result.append(k)
    return result

primes = sieve(100)
for p in primes:
    print(p)
