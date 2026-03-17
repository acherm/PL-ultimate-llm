defn fib (n)
  if (< n 2) n
    + (fib (- n 1)) (fib (- n 2))

defn main ()
  var i 0
  while (< i 10)
    println (fib i)
    = i (+ i 1)

main
