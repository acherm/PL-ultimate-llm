int fibonacci(int n)
  if n < 2
    return n
  else
    return fibonacci(n - 1) + fibonacci(n - 2)
  /if
/int

int main()
  for int i = 0; i < 10; i++
    print i, ": ", fibonacci(i), "\n"
  /for
  return 0
/int
