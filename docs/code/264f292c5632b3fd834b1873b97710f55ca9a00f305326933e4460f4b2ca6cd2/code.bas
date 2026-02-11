' Fibonacci Number Generator
' Calculates and displays Fibonacci numbers

input "Enter how many Fibonacci numbers to generate: "; n

a = 0
b = 1

print "Fibonacci sequence:"
print a

if n > 1 then
    print b
end if

for i = 3 to n
    c = a + b
    print c
    a = b
    b = c
next i

print
print "Done!"
end