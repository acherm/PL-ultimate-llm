int fib(int n) {
    if (n < 2) return n;
    return fib(n-1) + fib(n-2);
}

int i;
for (i = 0; i <= 10; i++) {
    printf("%d\n", fib(i));
}
