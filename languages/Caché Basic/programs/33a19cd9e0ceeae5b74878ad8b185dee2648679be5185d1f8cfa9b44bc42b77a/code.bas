' Fibonacci sequence in Cache Basic
' Demonstrates basic syntax: variables, loops, output
Sub Main()
    Dim a As Integer
    Dim b As Integer
    Dim c As Integer
    Dim i As Integer
    a = 0
    b = 1
    Print "Fibonacci sequence:"
    Print a
    Print b
    For i = 1 To 8
        c = a + b
        Print c
        a = b
        b = c
    Next i
End Sub
