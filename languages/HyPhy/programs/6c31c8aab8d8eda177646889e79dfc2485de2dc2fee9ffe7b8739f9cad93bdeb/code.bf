/* HyPhy Batch Language: Fibonacci sequence */

function fibonacci(n) {
    if (n <= 0) {
        return 0;
    }
    if (n == 1) {
        return 1;
    }
    a = 0;
    b = 1;
    for (i = 2; i <= n; i += 1) {
        c = a + b;
        a = b;
        b = c;
    }
    return b;
}

fprintf(stdout, "Fibonacci sequence:\n");
for (k = 0; k <= 10; k += 1) {
    fprintf(stdout, "F(", k, ") = ", fibonacci(k), "\n");
}
