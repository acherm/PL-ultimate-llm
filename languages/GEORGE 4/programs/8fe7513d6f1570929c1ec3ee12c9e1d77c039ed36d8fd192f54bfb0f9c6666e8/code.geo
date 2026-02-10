; Simple GEORGE 4 program to calculate factorial
; Input: N (number)
; Output: N! (factorial)

READ N ;
F = 1 ;
I = 1 ;
LOOP:
  IF I > N, EXIT ;
  F = F * I ;
  I = I + 1 ;
  JUMP LOOP ;
EXIT:
PRINT F ;
