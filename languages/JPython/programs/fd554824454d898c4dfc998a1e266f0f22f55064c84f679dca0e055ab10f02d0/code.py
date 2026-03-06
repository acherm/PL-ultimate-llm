# Hello World and Factorial in JPython
# JPython (later renamed Jython) runs Python on the JVM

print "Hello, World!"

def factorial(n):
    if n == 0:
        return 1
    return n * factorial(n - 1)

for i in range(1, 11):
    print i, "! =", factorial(i)
