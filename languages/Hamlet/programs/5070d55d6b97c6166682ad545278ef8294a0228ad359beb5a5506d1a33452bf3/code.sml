(* Fibonacci numbers - Hamlet (Standard ML) *)
fun fib 0 = 0
  | fib 1 = 1
  | fib n = fib (n - 1) + fib (n - 2)

val () =
  let
    val n = 10
    val fibs = List.tabulate (n, fib)
  in
    List.app (fn x => print (Int.toString x ^ "\n")) fibs
  end
