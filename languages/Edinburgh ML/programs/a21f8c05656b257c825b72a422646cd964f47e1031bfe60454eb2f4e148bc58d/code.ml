fun fact 0 = 1
  | fact n = n * fact (n - 1);

fun main() =
  let
    val n = 5
  in
    print("factorial(" ^ Int.toString(n) ^ ") = " ^ Int.toString(fact(n)) ^ "\n")
  end;
