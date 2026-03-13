// Fibonacci sequence in Adobe ExtendScript
// Demonstrates iterative computation in ExtendScript (Adobe JSX)

function fibonacci(n) {
    if (n <= 0) return 0;
    if (n === 1) return 1;
    var a = 0, b = 1;
    for (var i = 2; i <= n; i++) {
        var c = a + b;
        a = b;
        b = c;
    }
    return b;
}

var results = [];
for (var i = 0; i <= 10; i++) {
    results.push("fib(" + i + ") = " + fibonacci(i));
}

$.writeln(results.join("\n"));
