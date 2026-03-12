/* Parallel Fibonacci using CC++ (Compositional C++)
 * Demonstrates the par compound statement for parallel execution.
 */
#include <stdio.h>

int fib(int n) {
    if (n < 2) return n;
    int a, b;
    par {
        a = fib(n - 1);
        b = fib(n - 2);
    }
    return a + b;
}

int main() {
    int i;
    for (i = 0; i <= 10; i++) {
        printf("fib(%2d) = %d\n", i, fib(i));
    }
    return 0;
}
