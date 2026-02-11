Sub Main()
  Cls
  Print "Hello, World!"
  Print "Welcome to NSBasic"

  ' Create a button
  Button 1, "OK", 50, 100, 40, 20

  ' Wait for button press
  Do
    DoEvents
    If objClicked = 1 Then
      Print "Button clicked!"
      Exit Do
    End If
  Loop
End Sub
