begin
    fib = new(15, integer)
    fib(0) = 0
    fib(1) = 1
    do i = 2, 14
        fib(i) = fib(i-1) + fib(i-2)
    end do
    print(fib)
end
