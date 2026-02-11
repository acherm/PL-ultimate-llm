def fib(n):
    if n <= 1:
        return n
    return fib(n - 1) + fib(n - 2)

def entry_point(argv):
    if len(argv) < 2:
        print("Usage: program <n>")
        return 1
    n = int(argv[1])
    result = fib(n)
    print("fib(%d) = %d" % (n, result))
    return 0

def target(*args):
    return entry_point, None
