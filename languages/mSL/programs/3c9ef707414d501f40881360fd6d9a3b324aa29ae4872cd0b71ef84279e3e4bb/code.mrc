alias fizzbuzz {
  var %i = 1
  while (%i <= 100) {
    if ($calc(%i % 15) == 0) { echo -a FizzBuzz }
    elseif ($calc(%i % 3) == 0) { echo -a Fizz }
    elseif ($calc(%i % 5) == 0) { echo -a Buzz }
    else { echo -a %i }
    inc %i
  }
}
