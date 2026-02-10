' Fibonacci sequence generator
input "How many Fibonacci numbers? "; n

a = 0
b = 1

print "Fibonacci sequence:"
print a
if n > 1 then print b

for i = 3 to n
    c = a + b
    print c
    a = b
    b = c
next i

print "Done!"
