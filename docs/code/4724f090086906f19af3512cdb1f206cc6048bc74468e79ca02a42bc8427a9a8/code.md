function fib(n)
{
    if(n < 2)
        return n

    local a = 0
    local b = 1

    for(i: 2 .. n)
    {
        local temp = b
        b = a + b
        a = temp
    }

    return b
}

writefln("fib(10) = {}", fib(10))
