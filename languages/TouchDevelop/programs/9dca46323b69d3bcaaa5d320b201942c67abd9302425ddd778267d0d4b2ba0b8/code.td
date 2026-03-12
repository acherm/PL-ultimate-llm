// Fibonacci sequence calculator in TouchDevelop
action fibonacci(n : Number) returns Number
  if n <= 1 then
    return n
  end
  var a := 0
  var b := 1
  var i := 2
  while i <= n do
    var tmp := a + b
    a := b
    b := tmp
    i := i + 1
  end
  return b
end

action main()
  var i := 0
  while i <= 15 do
    wall→add text("fib(" + i→to string + ") = " + fibonacci(i)→to string)
    i := i + 1
  end
end
