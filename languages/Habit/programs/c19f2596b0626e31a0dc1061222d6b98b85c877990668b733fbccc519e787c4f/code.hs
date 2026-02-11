-- Factorial function in Habit
factorial :: Unsigned -> Unsigned
factorial n = if n == 0 then 1 else n * factorial (n - 1)

main :: M Unsigned
main = do
  let result = factorial 5
  return result
