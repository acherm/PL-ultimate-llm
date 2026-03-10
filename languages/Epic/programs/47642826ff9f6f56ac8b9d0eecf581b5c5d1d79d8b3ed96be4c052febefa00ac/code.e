include "Prelude.e"

fib(n : Int) -> Int =
    if n < 2 then n
    else fib(n - 1) + fib(n - 2);

main() -> Int = {
    let i : Int = 0 in {
        while (i <= 10) {
            putStr(intToString(fib(i)));
            putStr(" ");
            i = i + 1
        };
        putStrLn("");
        return 0
    }
}
