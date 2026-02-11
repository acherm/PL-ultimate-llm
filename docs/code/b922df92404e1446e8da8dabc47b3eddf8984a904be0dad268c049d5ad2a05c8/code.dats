fun fact (n: int): int =
  if n > 0 then n * fact (n - 1) else 1

implement main0 () = () where {
  val () = assertloc (fact 5 = 120)
}