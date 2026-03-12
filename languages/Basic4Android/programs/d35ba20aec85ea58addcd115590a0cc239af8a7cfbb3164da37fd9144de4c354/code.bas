Dim i As Int
For i = 1 To 100
    If i Mod 15 = 0 Then
        Log("FizzBuzz")
    Else If i Mod 3 = 0 Then
        Log("Fizz")
    Else If i Mod 5 = 0 Then
        Log("Buzz")
    Else
        Log(i)
    End If
Next
