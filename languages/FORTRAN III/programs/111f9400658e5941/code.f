C     FORTRAN III SAMPLE PROGRAM
      DIMENSION A(10)
      READ 100, N
100   FORMAT (I5)
      DO 10 I = 1, N
      READ 101, A(I)
101   FORMAT (F10.2)
10    CONTINUE
      SUM = 0.0
      DO 20 I = 1, N
      SUM = SUM + A(I)
20    CONTINUE
      AVG = SUM / FLOAT(N)
      WRITE (6,102) AVG
102   FORMAT (1X, 'AVERAGE = ', F10.2)
      STOP
      END
