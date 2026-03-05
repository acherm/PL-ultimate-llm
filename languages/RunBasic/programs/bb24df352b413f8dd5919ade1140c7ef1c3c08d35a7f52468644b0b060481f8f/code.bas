' Fibonacci sequence in Run BASIC
a = 0
b = 1
print "Fibonacci Sequence"
for i = 1 to 15
  print i; ": "; a
  temp = a + b
  a = b
  b = temp
next i
