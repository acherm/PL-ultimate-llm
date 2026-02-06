(* Factorial function in ML *)
fun factorial 0 = 1
  | factorial n = n * factorial (n - 1);

(* Power function *)
fun power (x, 0) = 1
  | power (x, n) = x * power (x, n - 1);

(* List operations *)
fun length [] = 0
  | length (x::xs) = 1 + length xs;

fun sum [] = 0
  | sum (x::xs) = x + sum xs;

(* Map function *)
fun map f [] = []
  | map f (x::xs) = f x :: map f xs;

(* Filter function *)
fun filter p [] = []
  | filter p (x::xs) =
    if p x then x :: filter p xs
    else filter p xs;

(* Example usage *)
val result1 = factorial 5;
val result2 = power (2, 10);
val result3 = length [1, 2, 3, 4, 5];
val result4 = sum [1, 2, 3, 4, 5];
val result5 = map (fn x => x * 2) [1, 2, 3, 4, 5];
val result6 = filter (fn x => x mod 2 = 0) [1, 2, 3, 4, 5, 6, 7, 8, 9, 10];
