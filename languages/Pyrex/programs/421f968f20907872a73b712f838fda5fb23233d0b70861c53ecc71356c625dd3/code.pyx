def fib(int n):
    """Calculate the nth Fibonacci number."""
    cdef int i
    cdef int a = 0
    cdef int b = 1
    cdef int temp

    if n <= 0:
        return 0
    elif n == 1:
        return 1

    for i from 2 <= i <= n:
        temp = a + b
        a = b
        b = temp

    return b

def fibonacci_list(int count):
    """Generate a list of the first count Fibonacci numbers."""
    result = []
    cdef int i
    for i from 0 <= i < count:
        result.append(fib(i))
    return result
