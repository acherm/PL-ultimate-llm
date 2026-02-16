sub fibonacci(n)
    var a = 0
    var b = 1
    var i = 0
    while i < n do
        print a
        var temp = a
        a = b
        b = temp + b
        i = i + 1
    end
end

fibonacci(10)