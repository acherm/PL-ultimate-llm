⍝ This is a comment in APL
⍝ Average function
avg ← {(+/⍵)÷⍴⍵}

⍝ Test with a vector
numbers ← 1 2 3 4 5 6 7 8 9 10

⍝ Calculate and display average
'Average: ', ⍕avg numbers

⍝ Sum of squares
'Sum of squares: ', ⍕+/numbers*2

⍝ Factorial using scan
'Factorial of 10: ', ⍕×/⍳10
