def fizzBuzz (n : Nat) : String :=
  if n % 15 == 0 then "FizzBuzz"
  else if n % 3 == 0 then "Fizz"
  else if n % 5 == 0 then "Buzz"
  else toString n

def main : IO Unit := do
  for i in List.range 20 do
    IO.println (fizzBuzz (i + 1))
