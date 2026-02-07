main:
  fib_a := 0
  fib_b := 1
  10.repeat:
    print fib_a
    next := fib_a + fib_b
    fib_a = fib_b
    fib_b = next
