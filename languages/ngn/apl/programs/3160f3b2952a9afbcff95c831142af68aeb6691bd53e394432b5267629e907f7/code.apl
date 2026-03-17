⍝ Quicksort in ngn/apl
qsort←{
  1≥≢⍵:⍵
  pivot←⍵[⌊2÷⍨≢⍵]
  (∇⍵[⍸⍵<pivot]),pivot,(∇⍵[⍸⍵>pivot])
}

⍝ Test with unsorted array
qsort 3 1 4 1 5 9 2 6 5 3 5

⍝ Sum of first 10 integers
+/⍳10

⍝ Outer product: multiplication table
∘.×⍨⍳5
