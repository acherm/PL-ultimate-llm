H DFTACTGRP(*NO) ACTGRP('MYACTGRP')
FMYFILE   IF   E           K DISK
D* Define variables
D Name            S             10A
C* Read the file
C     MYFILE    IF   E
C     READ      MYFILE
C     DOW       NOT %EOF(MYFILE)
C* Process each record
C     EVAL      Name = %TRIMR(Name)
C     WRITE     MYFILE
C     READ      MYFILE
C     ENDDO
C     SETON                                        LR