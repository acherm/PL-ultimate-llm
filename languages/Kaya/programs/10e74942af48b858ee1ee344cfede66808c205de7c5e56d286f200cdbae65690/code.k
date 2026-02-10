program factorial;

// Recursive factorial function
Int factorial(Int n) {
    if (n <= 1) {
        return 1;
    } else {
        return n * factorial(n - 1);
    }
}

Void main() {
    putStrLn("Factorial of 5: " + intToString(factorial(5)));
    putStrLn("Factorial of 10: " + intToString(factorial(10)));
}
