/* Fibonacci sequence in Open Object Rexx */
numeric digits 50

say "Fibonacci Sequence"
say copies("=", 40)

a = 0
b = 1
do i = 1 to 25
    say right(i, 3) ":" right(b, 20)
    temp = a + b
    a = b
    b = temp
end
