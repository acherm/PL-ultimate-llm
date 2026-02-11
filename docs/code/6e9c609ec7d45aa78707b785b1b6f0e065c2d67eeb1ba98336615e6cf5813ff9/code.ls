fizzbuzz = (n) ->
  for i from 1 til n
    switch
    case not i % 15 => 'FizzBuzz'
    case not i % 5 => 'Fizz'
    case not i % 3 => 'Buzz'
    default ' #{i}'

for fb to 20 => console.log fb