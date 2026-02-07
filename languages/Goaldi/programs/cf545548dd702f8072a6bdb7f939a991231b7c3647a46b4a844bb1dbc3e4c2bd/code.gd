# Fibonacci sequence generator in Goaldi
procedure main()
    every write(fib(1 to 20))
end

procedure fib(n)
    local a, b, c
    a := 0
    b := 1
    every 1 to n do {
        c := a + b
        a := b
        b := c
    }
    return a
end
