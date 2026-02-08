def fibonacci(n: int): int
    if n <= 1
        return n
    var a = 0
    var b = 1
    for i in range(2, n + 1)
        let c = a + b
        a = b
        b = c
    return b

[export]
def main()
    for i in range(0, 20)
        print("{fibonacci(i)} ")
    print("\n")
