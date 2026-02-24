Public Sub FizzBuzz()
    Dim n As Integer
    For n = 1 To 100
        If n Mod 15 = 0 Then
            Debug.Print "FizzBuzz"
        ElseIf n Mod 3 = 0 Then
            Debug.Print "Fizz"
        ElseIf n Mod 5 = 0 Then
            Debug.Print "Buzz"
        Else
            Debug.Print n
        End If
    Next n
End Sub
