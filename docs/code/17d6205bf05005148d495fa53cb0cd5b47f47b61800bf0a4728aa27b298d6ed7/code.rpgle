H DFTACTGRP(*NO) ACTGRP('QILE')
FMYFILE  IF   E           K DISK
D* Define a data structure
D MYDS           DS
D   FIELD1                 10A
D   FIELD2                 10A
D   FIELD3                 10A
C* Read a record from the file
C     MYFILE    CHAIN     MYDS
C* Check if record is found
C     *INFOUND IFEQ      *OFF
C* Write a message if not found
C     'Record not found' DSPLY
C     ENDIF
C* End of program
C                   SETON                     LR