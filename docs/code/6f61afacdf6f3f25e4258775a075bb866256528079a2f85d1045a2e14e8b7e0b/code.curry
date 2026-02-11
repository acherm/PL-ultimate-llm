fizzbuzz 0 = ""
fizzbuzz n = (if mod n 15 == 0 then "FizzBuzz" else
               if mod n 3 == 0 then "Fizz" else
               if mod n 5 == 0 then "Buzz" else show n) ++
              (if n==1 then "" else " " ++ fizzbuzz (n-1))

main = putStr (reverse (fizzbuzz 100))