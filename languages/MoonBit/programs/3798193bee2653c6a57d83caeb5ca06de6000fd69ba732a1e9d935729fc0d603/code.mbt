fn fib(n : Int) -> Int {
  if n <= 1 {
    n
  } else {
    fib(n - 1) + fib(n - 2)
  }
}

fn main {
  let n = 10
  println("Fibonacci(\{n}) = \{fib(n)}")
}
