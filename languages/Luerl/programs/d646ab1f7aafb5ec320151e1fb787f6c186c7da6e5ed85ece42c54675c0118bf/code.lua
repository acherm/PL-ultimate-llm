-- Factorial function in Lua
function factorial(n)
    if n == 0 then
        return 1
    else
        return n * factorial(n - 1)
    end
end

-- Calculate and print factorials
for i = 0, 10 do
    print(string.format("%d! = %d", i, factorial(i)))
end
