sub Main()
    print "Hello from BrightScript!"
    numbers = [1, 2, 3, 4, 5]
    sum = 0
    for each num in numbers
        sum = sum + num
    end for
    print "Sum of numbers: "; sum
end sub
