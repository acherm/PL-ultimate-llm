(*
** Fibonacci sequence in ATS2
*)
#include "share/atspre_staload.hats"

fun fib (n: int): int =
  if n <= 1 then n
  else fib(n-1) + fib(n-2)

implement main0 () = {
  val () = println! ("fib(0)  = ", fib 0)
  val () = println! ("fib(1)  = ", fib 1)
  val () = println! ("fib(5)  = ", fib 5)
  val () = println! ("fib(10) = ", fib 10)
  val () = println! ("fib(15) = ", fib 15)
}
