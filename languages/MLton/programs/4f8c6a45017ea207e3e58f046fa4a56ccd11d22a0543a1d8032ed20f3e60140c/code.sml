fun fact 0 = 1
  | fact n = n * fact (n - 1)

val () = print (Int.toString (fact 10) ^ "\n")
