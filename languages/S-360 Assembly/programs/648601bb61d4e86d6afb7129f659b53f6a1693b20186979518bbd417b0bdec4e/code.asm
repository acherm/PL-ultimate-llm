HELLO    CSECT
         STM   14,12,12(13)
         BALR  12,0
         USING *,12
         LA    15,SAVEAREA
         ST    13,4(15)
         ST    15,8(13)
         LR    13,15
         WTO   'HELLO WORLD'
         L     13,4(13)
         LM    14,12,12(13)
         SR    15,15
         BR    14
SAVEAREA DS    18F
         END   HELLO
