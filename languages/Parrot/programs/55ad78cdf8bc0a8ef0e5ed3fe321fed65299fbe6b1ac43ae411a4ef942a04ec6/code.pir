.sub fib
    .param int n
    .local int a
    .local int b
    .local int tmp
    a = 0
    b = 1
    if n == 0 goto done_a
    if n == 1 goto done_b
loop:
    tmp = a + b
    a = b
    b = tmp
    n = n - 1
    if n > 1 goto loop
done_b:
    .return(b)
done_a:
    .return(a)
.end

.sub main :main
    .local int i
    i = 0
top:
    if i > 10 goto end
    $I0 = fib(i)
    print "fib("
    print i
    print ") = "
    say $I0
    i = i + 1
    goto top
end:
.end
