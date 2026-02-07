def fibonacci(n):
    if n <= 1:
        return n
    else:
        return fibonacci(n - 1) + fibonacci(n - 2)

def main():
    console.log("Fibonacci sequence:")
    for i in range(10):
        console.log(f"F({i}) = {fibonacci(i)}")

main()
