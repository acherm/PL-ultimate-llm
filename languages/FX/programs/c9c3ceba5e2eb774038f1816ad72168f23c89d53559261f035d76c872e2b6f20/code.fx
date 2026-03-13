(* FX Programming Language - MIT LCS *)
(* Example: Factorial and Fibonacci using FX's ML-like syntax *)

(* Factorial: pure recursive function *)
fun fact (n : int) : int =
  if n = 0 then 1
  else n * fact (n - 1)

(* Fibonacci: pure recursive function *)
fun fib (n : int) : int =
  if n = 0 then 0
  else if n = 1 then 1
  else fib (n - 1) + fib (n - 2)

(* Print first 10 Fibonacci numbers *)
fun print_fibs (i : int) : unit =
  if i > 10 then ()
  else
    (print_int (fib i);
     print " ";
     print_fibs (i + 1))

fun main () : unit =
  (print "Fibonacci: ";
   print_fibs 0;
   print "\n";
   print "10! = ";
   print_int (fact 10);
   print "\n")

val _ = main ()
