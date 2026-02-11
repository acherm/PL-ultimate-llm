* Simple addition program for IBM 7090
* Adds two numbers and stores result
       ORG  100
START  CLA  NUM1    CLEAR AC AND LOAD NUM1
       ADD  NUM2    ADD NUM2 TO AC
       STO  RESULT  STORE RESULT
       HTR          HALT AND TRANSFER
NUM1   DEC  42      FIRST NUMBER
NUM2   DEC  58      SECOND NUMBER
RESULT BSS  1       RESULT STORAGE
       END  START
