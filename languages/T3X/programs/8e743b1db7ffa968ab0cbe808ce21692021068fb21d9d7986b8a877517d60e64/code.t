fib(n) do var x1, x2, i, t;
    x1 := 0;
    x2 := 1;
    for (i=1, n) do
        t := x2;
        x2 := x2 + x1;
        x1 := t;
    end
    return x2;
end

do var i;
    for (i=1, 11) do
        writes(ntoa(fib(i)));
        writes("\n");
    end
end