// Compute Fibonacci numbers using Panorama scripting language
// Panorama X procedure demonstrating loops and local variables

local n, a, b, temp, result
n = 10
a = 0
b = 1
result = "Fibonacci sequence: " + str(a) + ", " + str(b)

loop
    if n <= 2, exitloop
    temp = a + b
    a = b
    b = temp
    result = result + ", " + str(b)
    n = n - 1
endloop

message result
