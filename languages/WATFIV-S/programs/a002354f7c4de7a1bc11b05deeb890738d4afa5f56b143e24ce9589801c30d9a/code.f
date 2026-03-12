C     WATFIV-S BUBBLE SORT PROGRAM
C     DEMONSTRATES STRUCTURED PROGRAMMING EXTENSIONS
      INTEGER ARRAY(10), N, I, TEMP
      LOGICAL SWAPPED
      DATA ARRAY /64, 34, 25, 12, 22, 11, 90, 45, 33, 1/
      N = 10
      SWAPPED = .TRUE.
      WHILE (SWAPPED) DO
        SWAPPED = .FALSE.
        DO 20 I = 1, N-1
          IF (ARRAY(I) .GT. ARRAY(I+1)) THEN
            TEMP = ARRAY(I)
            ARRAY(I) = ARRAY(I+1)
            ARRAY(I+1) = TEMP
            SWAPPED = .TRUE.
          END IF
   20   CONTINUE
      END WHILE
      DO 30 I = 1, N
        WRITE(6,*) ARRAY(I)
   30 CONTINUE
      STOP
      END
