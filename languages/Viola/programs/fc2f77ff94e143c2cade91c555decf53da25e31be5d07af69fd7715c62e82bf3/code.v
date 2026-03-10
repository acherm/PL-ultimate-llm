/* Fibonacci sequence in Viola scripting language
   Viola was a hypertext scripting language for the ViolaWWW browser,
   one of the first graphical web browsers (early 1990s). */

func fib(n) {
    if (n <= 0) {
        return 0;
    }
    if (n == 1) {
        return 1;
    }
    return fib(n - 1) + fib(n - 2);
}

var i;
i = 0;
while (i <= 10) {
    print(fib(i));
    i = i + 1;
}
