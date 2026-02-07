class Fibonacci {
  def self fib: n {
    n <= 1 if_true: {
      n
    } else: {
      (self fib: (n - 1)) + (self fib: (n - 2))
    }
  }
}

10 times: |i| {
  "Fibonacci(" ++ i ++ ") = " ++ (Fibonacci fib: i) println
}