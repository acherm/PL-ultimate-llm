* IBM 1130 Assembly - Simple Addition Program
* This program adds two numbers and stores the result

       ORG  0100
START  LDX  1 NUM1     Load first number into Index 1
       LDX  2 NUM2     Load second number into Index 2
       STX  1 TEMP     Store first number in temp
       LD   TEMP       Load temp into accumulator
       A    NUM2       Add second number
       STO  RESULT     Store result
       WAIT            Halt processor
       BSC  I START    Return to start

NUM1   DC   5          First number (5)
NUM2   DC   7          Second number (7)
TEMP   BSS  1          Temporary storage
RESULT BSS  1          Result storage

       END  START