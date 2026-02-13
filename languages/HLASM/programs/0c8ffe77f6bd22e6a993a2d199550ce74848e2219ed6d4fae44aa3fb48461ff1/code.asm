HELLO    CSECT
         STM   14,12,12(13)
         BALR  12,0
         USING *,12
         ST    13,SAVEAREA+4
         LA    13,SAVEAREA

         WTO   'HELLO, WORLD!',ROUTCDE=11

         L     13,SAVEAREA+4
         LM    14,12,12(13)
         SR    15,15
         BR    14

SAVEAREA DS    18F
         END   HELLO
