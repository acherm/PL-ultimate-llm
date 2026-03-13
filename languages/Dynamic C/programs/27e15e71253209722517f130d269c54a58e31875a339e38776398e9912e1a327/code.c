// Fibonacci sequence in Dynamic C
// Runs on Rabbit processor boards

#use "stdio.lib"

void main(void)
{
    int n;
    long fib, f0, f1;

    f0 = 0L;
    f1 = 1L;

    for (n = 0; n <= 20; n++) {
        printf("F(%2d) = %ld\n", n, f0);
        fib = f0 + f1;
        f0 = f1;
        f1 = fib;
    }
}
