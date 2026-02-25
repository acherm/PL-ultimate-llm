' FizzBuzz in AMOS Basic
For N = 1 To 100
  If N Mod 15 = 0
    Print "FizzBuzz"
  Else
    If N Mod 3 = 0
      Print "Fizz"
    Else
      If N Mod 5 = 0
        Print "Buzz"
      Else
        Print N
      End If
    End If
  End If
Next N
