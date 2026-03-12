fun fib 0 = 0
  | fib 1 = 1
  | fib n = fib (n - 1) + fib (n - 2)

fun printFibs i =
    if i > 10 then ()
    else
        ( print ("fib(" ^ Int.toString i ^ ") = " ^ Int.toString (fib i) ^ "\n")
        ; printFibs (i + 1)
        )

val () = printFibs 0
