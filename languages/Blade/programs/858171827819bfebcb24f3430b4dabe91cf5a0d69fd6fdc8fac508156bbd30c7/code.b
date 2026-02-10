# Fibonacci sequence in Blade
# Computes and prints the first 20 Fibonacci numbers

def fibonacci(n) {
  var a = 0
  var b = 1
  var result = []

  for var i = 0; i < n; i++ {
    result.append(a)
    var temp = a + b
    a = b
    b = temp
  }

  return result
}

var fibs = fibonacci(20)
for var i = 0; i < fibs.length(); i++ {
  echo 'fib(${i}) = ${fibs[i]}'
}