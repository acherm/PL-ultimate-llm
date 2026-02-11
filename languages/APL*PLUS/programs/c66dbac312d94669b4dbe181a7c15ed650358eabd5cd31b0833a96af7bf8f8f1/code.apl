⍝ Factorial function
fact←{⍵=0:1 ⋄ ⍵×∇⍵-1}

⍝ Test cases
fact 5
fact 10