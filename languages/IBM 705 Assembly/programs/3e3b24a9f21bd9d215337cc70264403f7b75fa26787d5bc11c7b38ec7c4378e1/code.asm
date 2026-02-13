* IBM 705 Assembly - Sum Array Example
* This program sums an array of numbers
*
       ORG  2000
START  CLA  ZERO
       STO  SUM
       CLA  COUNT
       STO  INDEX
LOOP   CLT  INDEX
       JZ   DONE
       CLA  INDEX
       SUB  ONE
       STO  INDEX
       CLA  INDEX
       ADD  ARRAY
       STO  TEMP
       CLT  TEMP
       CLA  0
       ADD  SUM
       STO  SUM
       J    LOOP
DONE   CLA  SUM
       HLT
*
* Data area
*
ZERO   DEC  0
ONE    DEC  1
COUNT  DEC  5
SUM    DEC  0
INDEX  DEC  0
TEMP   DEC  0
ARRAY  DEC  10
       DEC  20
       DEC  30
       DEC  40
       DEC  50
       END  START
