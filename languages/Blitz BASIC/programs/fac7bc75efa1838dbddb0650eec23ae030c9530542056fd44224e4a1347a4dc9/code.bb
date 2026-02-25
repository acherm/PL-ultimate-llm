Function Fibonacci(n)
  If n < 2 Then Return n
  Return Fibonacci(n-1) + Fibonacci(n-2)
End Function

For i = 0 To 10
  Print Fibonacci(i)
Next
WaitKey
