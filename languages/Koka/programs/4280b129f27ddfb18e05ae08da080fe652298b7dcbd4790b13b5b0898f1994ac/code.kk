public fun fib( n : int ) : div int
  if n <= 1 then n else fib(n-1) + fib(n-2)

public fun main()
  println("fib(10) = " + fib(10).show())
  val t0 = time()
  val x  = fib(35)
  val t1 = time()
  println("fib(35) = " + x.show() + ", took: " + (t1 - t0).show() + " seconds")