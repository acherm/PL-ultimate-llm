-- Fibonacci sequence generator with Luau type annotations
type NumberArray = {number}

local function fibonacci(n: number): NumberArray
    local result: NumberArray = {}
    local a, b = 0, 1

    for i = 1, n do
        table.insert(result, a)
        a, b = b, a + b
    end

    return result
end

local function printSequence(sequence: NumberArray): ()
    for i, v in ipairs(sequence) do
        print(string.format("F(%d) = %d", i - 1, v))
    end
end

-- Generate and print first 10 Fibonacci numbers
local fib = fibonacci(10)
printSequence(fib)
