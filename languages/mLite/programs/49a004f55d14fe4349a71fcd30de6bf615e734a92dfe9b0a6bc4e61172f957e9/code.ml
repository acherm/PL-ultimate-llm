fun fib 0 = 0
  | fib 1 = 1
  | fib n = fib (n-1) + fib (n-2)

fun show_fibs [] = ()
  | show_fibs (x::xs) = (write (fib x); nl (); show_fibs xs)

do show_fibs [0,1,2,3,4,5,6,7,8,9,10]
