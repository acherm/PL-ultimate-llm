(* Fibonacci function in Caml Light *)
let rec fib n =
  if n <= 1 then n
  else fib (n - 1) + fib (n - 2);;

(* Print first 10 Fibonacci numbers *)
for i = 0 to 9 do
  print_int (fib i);
  print_string " "
done;;
print_newline();;
