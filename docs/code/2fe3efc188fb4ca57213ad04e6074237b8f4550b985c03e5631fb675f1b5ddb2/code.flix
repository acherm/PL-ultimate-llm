def main(): Unit = {
    let n = 100;
    forEach(i <- Range.range(1, n + 1)) {
        match (i `mod` 3, i `mod` 5) {
            case (0, 0) => println("FizzBuzz")
            case (0, _) => println("Fizz")
            case (_, 0) => println("Buzz")
            case _     => println(${i})
        }
    }
}