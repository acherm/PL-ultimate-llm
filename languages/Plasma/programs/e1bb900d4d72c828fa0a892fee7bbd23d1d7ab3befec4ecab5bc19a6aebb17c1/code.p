module Fibonacci

entrypoint
func main() uses IO -> Int {
    print!(fibonacci(10) |> int_to_string |> append_string("\n"))
    return 0
}

func fibonacci(n : Int) -> Int {
    if (n < 2) {
        return n
    } else {
        return fibonacci(n - 1) + fibonacci(n - 2)
    }
}
