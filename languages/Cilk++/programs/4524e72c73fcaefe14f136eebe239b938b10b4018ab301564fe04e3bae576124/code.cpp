#include <cilk/cilk.h>
#include <stdio.h>

int fib(int n)
{
    if (n < 2)
        return n;

    int x = cilk_spawn fib(n-1);
    int y = fib(n-2);
    cilk_sync;
    return x + y;
}

int main(void)
{
    int result = fib(30);
    printf("Fibonacci of 30 is %d\n", result);
    return 0;
}
