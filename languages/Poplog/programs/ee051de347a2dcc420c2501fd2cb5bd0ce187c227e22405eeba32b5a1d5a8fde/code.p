define factorial(n);
    if n <= 1 then
        1
    else
        n * factorial(n - 1)
    endif
enddefine;

factorial(5) =>
