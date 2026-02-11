* IBM 1620 Assembly - Addition Program
* Add two numbers and store result
       36 00100 49 16000         READ  NUM1
       36 00106 49 16012         READ  NUM2
       21 00112 16000 16012 16024 ADD   NUM1,NUM2,RESULT
       37 00124 46 16024         WRITE RESULT
       48 00130                  HALT
       00 16000                  NUM1   DS 12
       00 16012                  NUM2   DS 12
       00 16024                  RESULT DS 12
