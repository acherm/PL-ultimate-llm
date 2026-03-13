class Fibonacci {
  static Int fib(Int n) {
    if (n < 2) return n
    return fib(n - 1) + fib(n - 2)
  }

  static Void main() {
    (0..14).each |n| { echo(fib(n)) }
  }
}
