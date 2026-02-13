* Simple ASSIST program to add two numbers
         USING *,15
         XREAD NUM1,NUM2
         L     1,NUM1
         A     1,NUM2
         ST    1,SUM
         XPRNT SUM,12
         BR    14
NUM1     DS    F
NUM2     DS    F
SUM      DS    F
         END
