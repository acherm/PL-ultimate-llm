∇ Z←FIBO N;I
⍝ Compute Fibonacci sequence of length N using iteration
  Z←N⍴0
  →(N<1)/EXIT
  Z[1]←0
  →(N<2)/EXIT
  Z[2]←1
  I←3
LP:→(I>N)/EXIT
  Z[I]←Z[I-1]+Z[I-2]
  I←I+1
  →LP
EXIT:
∇

⎕←FIBO 10
