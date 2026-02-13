defn factorial (n)
  if (<= n 1)
    1
    * n
      factorial (- n 1)

defn main! ()
  println "Factorial of 5:"
  println $ factorial 5
  println "Factorial of 10:"
  println $ factorial 10
