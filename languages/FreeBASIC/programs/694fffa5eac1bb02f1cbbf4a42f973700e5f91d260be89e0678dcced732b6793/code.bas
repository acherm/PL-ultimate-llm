Function factorial (n As UInteger) As ULongInt
  If n <= 1 Then
    Return 1
  Else
    Return n * factorial(n-1)
  End If
End Function

Print "Factorials:"
For i As Integer = 0 To 10
  Print Using "#: ###..."; i; factorial(i)
Next
Sleep
End