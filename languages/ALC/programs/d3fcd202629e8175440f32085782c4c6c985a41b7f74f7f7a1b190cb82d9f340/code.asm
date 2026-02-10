HELLO    CSECT
         STM   14,12,12(13)
         BALR  12,0
         USING *,12
         LA    1,MSG
         WTO   MF=(E,(1))
         LM    14,12,12(13)
         BR    14
MSG      DC    AL2(MSGL,0)
         DC    C'HELLO WORLD'
MSGL     EQU   *-MSG
         END   HELLO
