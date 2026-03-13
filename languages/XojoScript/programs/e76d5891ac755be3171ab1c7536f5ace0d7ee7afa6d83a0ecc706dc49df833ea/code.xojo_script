// XojoScript: compute Fibonacci numbers recursively
Function Fibonacci(n As Integer) As Integer
  If n <= 1 Then
    Return n
  End If
  Return Fibonacci(n - 1) + Fibonacci(n - 2)
End Function

Dim i As Integer
For i = 0 To 10
  Print "Fibonacci(" + CStr(i) + ") = " + CStr(Fibonacci(i))
Next