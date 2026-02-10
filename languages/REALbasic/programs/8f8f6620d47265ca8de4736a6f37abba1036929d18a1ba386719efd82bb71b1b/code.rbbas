Dim numbers() As Integer
Dim i As Integer
Dim sum As Integer
Dim average As Double

// Initialize array with values
numbers.Append(10)
numbers.Append(20)
numbers.Append(30)
numbers.Append(40)
numbers.Append(50)

// Calculate sum
sum = 0
For i = 0 To numbers.Ubound
  sum = sum + numbers(i)
Next

// Calculate average
average = sum / (numbers.Ubound + 1)

// Display results
MsgBox "Sum: " + Str(sum) + Chr(13) + "Average: " + Str(average)
