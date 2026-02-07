mata:
void fibonacci(real scalar n)
{
    real scalar i
    real colvector fib

    fib = J(n, 1, 0)
    fib[1] = 1
    if (n > 1) fib[2] = 1

    for (i=3; i<=n; i++) {
        fib[i] = fib[i-1] + fib[i-2]
    }

    printf("Fibonacci sequence:\n")
    for (i=1; i<=n; i++) {
        printf("%f ", fib[i])
    }
    printf("\n")
}

fibonacci(10)
end