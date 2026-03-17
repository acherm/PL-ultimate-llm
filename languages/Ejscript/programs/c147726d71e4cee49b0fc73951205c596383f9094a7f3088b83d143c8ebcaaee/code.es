/*
    Ejscript factorial example
    Ejscript is an ECMAScript-compatible scripting language for embedded systems.
*/

function factorial(n: Number): Number {
    if (n <= 1) {
        return 1
    }
    return n * factorial(n - 1)
}

for (var i = 1; i <= 10; i++) {
    print("factorial(" + i + ") = " + factorial(i))
}
