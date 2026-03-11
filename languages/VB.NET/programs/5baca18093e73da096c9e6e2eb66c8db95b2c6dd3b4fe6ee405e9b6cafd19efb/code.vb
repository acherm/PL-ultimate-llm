Module Fibonacci
    Function Fib(n As Integer) As Long
        If n < 2 Then Return n
        Dim a As Long = 0
        Dim b As Long = 1
        For i As Integer = 2 To n
            Dim c As Long = a + b
            a = b
            b = c
        Next
        Return b
    End Function

    Sub Main()
        For i As Integer = 0 To 15
            Console.WriteLine("Fib(" & i & ") = " & Fib(i))
        Next
    End Sub
End Module
