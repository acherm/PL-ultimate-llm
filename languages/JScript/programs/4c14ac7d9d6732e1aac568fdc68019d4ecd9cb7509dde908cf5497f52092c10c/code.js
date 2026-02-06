// JScript Hello World with WScript
WScript.Echo("Hello, World!");

// Calculate factorial
function factorial(n) {
    if (n <= 1) return 1;
    return n * factorial(n - 1);
}

// Display factorial of 5
WScript.Echo("Factorial of 5 is: " + factorial(5));