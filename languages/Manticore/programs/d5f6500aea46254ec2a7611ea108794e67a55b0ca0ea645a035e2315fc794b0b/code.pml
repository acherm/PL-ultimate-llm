fun pfib (n : int) =
  if n < 2 then n
  else let
    val (x, y) = (| pfib(n-1), pfib(n-2) |)
  in
    x + y
  end

val result = pfib 10
val () = print(Int.toString result ^ "\n")
