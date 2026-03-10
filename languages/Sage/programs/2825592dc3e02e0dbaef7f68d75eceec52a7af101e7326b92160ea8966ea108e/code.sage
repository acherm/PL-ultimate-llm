# Prime factorization and symbolic computation in SageMath
n = 123456789
print('Factorization of', n, ':', factor(n))

# List primes up to 50
print('Primes up to 50:', list(primes(50)))

# Symbolic computation: find roots of a polynomial
x = var('x')
f = x^3 - 3*x + 2
print('Roots of x^3 - 3x + 2:', f.roots())

# Numerical integration
result = numerical_integral(sin(x), 0, pi)
print('Integral of sin(x) from 0 to pi:', result[0])
