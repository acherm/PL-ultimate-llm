def fibonacci(n: int) -> int:
    if n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fibonacci(n - 1) + fibonacci(n - 2)

i: int = 0
while i < 10:
    print(fibonacci(i))
    i = i + 1
