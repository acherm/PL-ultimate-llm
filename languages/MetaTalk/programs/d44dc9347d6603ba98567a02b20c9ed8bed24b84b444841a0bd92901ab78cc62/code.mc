on startup
  repeat with x = 1 to 100
    if x mod 15 = 0 then
      put "FizzBuzz"
    else if x mod 3 = 0 then
      put "Fizz"
    else if x mod 5 = 0 then
      put "Buzz"
    else
      put x
    end if
  end repeat
  quit
end startup
