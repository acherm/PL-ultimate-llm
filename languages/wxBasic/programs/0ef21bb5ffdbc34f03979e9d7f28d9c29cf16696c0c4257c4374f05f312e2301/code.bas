' Bubble sort in wxBasic

Sub BubbleSort(a() As Integer, n As Integer)
    Dim i As Integer
    Dim j As Integer
    Dim temp As Integer
    For i = 0 To n - 2
        For j = 0 To n - 2 - i
            If a(j) > a(j + 1) Then
                temp = a(j)
                a(j) = a(j + 1)
                a(j + 1) = temp
            End If
        Next j
    Next i
End Sub

Dim nums(9) As Integer
Dim i As Integer
nums(0) = 64
nums(1) = 34
nums(2) = 25
nums(3) = 12
nums(4) = 22
nums(5) = 11
nums(6) = 90
nums(7) = 55
nums(8) = 44
nums(9) = 7

BubbleSort(nums(), 10)

Print "Sorted:"
For i = 0 To 9
    Print nums(i)
Next i
