function! Fibonacci(n)
    if a:n < 2
        return a:n
    endif
    return Fibonacci(a:n - 1) + Fibonacci(a:n - 2)
endfunction

for i in range(0, 10)
    echo Fibonacci(i)
endfor
