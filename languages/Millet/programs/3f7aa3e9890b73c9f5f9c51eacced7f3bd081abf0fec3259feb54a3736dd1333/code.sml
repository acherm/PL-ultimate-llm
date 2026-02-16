(* Factorial function using pattern matching *)
fun factorial 0 = 1
  | factorial n = n * factorial (n - 1)

(* List operations *)
fun length [] = 0
  | length (_::xs) = 1 + length xs

fun map f [] = []
  | map f (x::xs) = f x :: map f xs

(* Main computation *)
val result = factorial 5
val nums = [1, 2, 3, 4, 5]
val doubled = map (fn x => x * 2) nums
