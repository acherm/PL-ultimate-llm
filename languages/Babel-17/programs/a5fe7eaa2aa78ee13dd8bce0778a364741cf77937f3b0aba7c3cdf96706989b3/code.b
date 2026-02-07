def factorial
  case 0 -> 1
  case n -> n * factorial (n - 1)
end

println (factorial 5)
println (factorial 10)
