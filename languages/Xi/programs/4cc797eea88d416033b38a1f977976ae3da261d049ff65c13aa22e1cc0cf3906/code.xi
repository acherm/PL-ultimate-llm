use io
use conv

// Compute factorial iteratively
factorial(n: int): int {
    result: int = 1
    i: int = 2
    while i <= n {
        result = result * i
        i = i + 1
    }
    return result
}

main(args: int[][]) {
    i: int = 0
    while i <= 10 {
        print(unparseInt(i))
        print("! = ")
        println(unparseInt(factorial(i)))
        i = i + 1
    }
}
