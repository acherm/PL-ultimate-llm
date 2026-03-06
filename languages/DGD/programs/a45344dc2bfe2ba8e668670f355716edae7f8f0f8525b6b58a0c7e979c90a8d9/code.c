/* fibonacci.c - Fibonacci numbers in DGD/LPC */
int fibonacci(int n) {
    if (n <= 1) {
        return n;
    }
    return fibonacci(n - 1) + fibonacci(n - 2);
}

string int_to_string(int n) {
    return (string) n;
}

static void create() {
    int i;
    int result;

    for (i = 0; i <= 10; i++) {
        result = fibonacci(i);
        write("fib(" + int_to_string(i) + ") = " + int_to_string(result) + "\n");
    }
}
