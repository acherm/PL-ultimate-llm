       ORG  1000
START  CLEAR  SUM
       READ   CARD1
       A      NUM1,SUM
       READ   CARD2
       A      NUM2,SUM
       WRITE  SUM
       HALT
SUM    DS     5
NUM1   DS     5
NUM2   DS     5
CARD1  DCW    @12345@
CARD2  DCW    @67890@
       END    START