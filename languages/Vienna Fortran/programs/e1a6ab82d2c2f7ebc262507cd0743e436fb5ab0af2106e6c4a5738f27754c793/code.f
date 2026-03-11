      PROGRAM VECT_ADD
C     Vienna Fortran example: distributed vector addition
      INTEGER N
      PARAMETER (N = 100)
      REAL A(N), B(N), C(N)
      INTEGER I
C
C$VF  DISTRIBUTE A(BLOCK)
C$VF  DISTRIBUTE B(BLOCK)
C$VF  DISTRIBUTE C(BLOCK)
C
      DO 10 I = 1, N
        A(I) = FLOAT(I)
        B(I) = FLOAT(N + 1 - I)
   10 CONTINUE
C
      DO 20 I = 1, N
        C(I) = A(I) + B(I)
   20 CONTINUE
C
      PRINT *, 'C(1) =', C(1)
      PRINT *, 'C(N) =', C(N)
      END