// Fibonacci sequence in AppGameKit BASIC
SetWindowTitle("Fibonacci Sequence")

n = 20
a = 0
b = 1

Print("Fibonacci Sequence (first " + Str(n) + " terms):")

For i = 1 To n
    Print(Str(a))
    temp = a + b
    a = b
    b = temp
Next i

Sync()
WaitKey()
