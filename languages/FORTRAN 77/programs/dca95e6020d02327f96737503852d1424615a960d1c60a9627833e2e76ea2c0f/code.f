      PROGRAM FIBONACCI
C     Classic FORTRAN 77 program to compute Fibonacci numbers
      INTEGER N, I, FIB, PREV, CURR, TEMP

      PRINT *, 'Enter the number of Fibonacci numbers to compute:'
      READ *, N

      IF (N .LE. 0) THEN
          PRINT *, 'Please enter a positive integer'
          STOP
      END IF

      PREV = 0
      CURR = 1

      PRINT *, 'Fibonacci sequence:'

      DO 10 I = 1, N
          IF (I .EQ. 1) THEN
              FIB = 0
          ELSE IF (I .EQ. 2) THEN
              FIB = 1
          ELSE
              FIB = PREV + CURR
              TEMP = CURR
              CURR = FIB
              PREV = TEMP
          END IF
          PRINT *, 'F(', I, ') = ', FIB
   10 CONTINUE

      END
