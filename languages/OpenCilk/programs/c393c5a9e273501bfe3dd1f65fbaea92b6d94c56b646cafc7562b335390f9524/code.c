#include <stdio.h>
#include <stdlib.h>
#include <cilk/cilk.h>

long fib(long n) {
    if (n < 2) return n;
    long x = cilk_spawn fib(n - 1);
    long y = fib(n - 2);
    cilk_sync;
    return x + y;
}

int main(int argc, char *argv[]) {
    long n = (argc > 1) ? atol(argv[1]) : 10;
    printf("fib(%ld) = %ld\n", n, fib(n));
    return 0;
}
