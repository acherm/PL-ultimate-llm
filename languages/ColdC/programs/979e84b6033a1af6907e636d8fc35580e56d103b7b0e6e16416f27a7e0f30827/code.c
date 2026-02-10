// Fibonacci calculator method
// Returns the nth Fibonacci number

var n, a, b, temp, i;

n = args[1];

if (n < 0)
    throw(~range, "Argument must be non-negative");

if (n <= 1)
    return n;

a = 0;
b = 1;

for i in [2 .. n] {
    temp = a + b;
    a = b;
    b = temp;
}

return b;
