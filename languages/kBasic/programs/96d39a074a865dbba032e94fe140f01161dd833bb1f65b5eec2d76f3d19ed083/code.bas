' Fibonacci sequence in kBasic
Dim a As Integer
Dim b As Integer
Dim temp As Integer
Dim i As Integer

a = 0
b = 1
Print "Fibonacci sequence (first 10 terms):"
Print a
Print b
For i = 3 To 10
    temp = a + b
    a = b
    b = temp
    Print b
Next i
