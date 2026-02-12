Sub Process_Globals
    Private Timer1 As Timer
    Private Counter As Int
End Sub

Sub AppStart (Args() As String)
    Counter = 0
    Timer1.Initialize("Timer1", 1000)
    Timer1.Enabled = True
    StartMessageLoop
End Sub

Sub Timer1_Tick
    Counter = Counter + 1
    Log("Counter: " & Counter)
    If Counter = 10 Then
        Timer1.Enabled = False
        StopMessageLoop
    End If
End Sub
