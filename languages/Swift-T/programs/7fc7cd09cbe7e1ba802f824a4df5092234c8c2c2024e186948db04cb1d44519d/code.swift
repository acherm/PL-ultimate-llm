import io;

(int result) factorial(int n) {
    if (n <= 1) {
        result = 1;
    } else {
        result = n * factorial(n-1);
    }
}

main {
    foreach i in [1:11] {
        printf("%i! = %i\n", i, factorial(i));
    }
}
