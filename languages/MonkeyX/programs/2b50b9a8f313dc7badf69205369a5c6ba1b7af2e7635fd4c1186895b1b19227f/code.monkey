Function fib:Int(n:Int)
    If n < 2 Then Return n
    Return fib(n-1) + fib(n-2)
End Function

Function Main:Int()
    For Local i:Int = 0 To 10
        Print fib(i)
    Next
    Return 0
End Function