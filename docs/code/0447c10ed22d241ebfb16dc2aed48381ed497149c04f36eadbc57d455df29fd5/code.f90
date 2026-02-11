      PROGRAM HEAT_EQ
      IMPLICIT NONE
      INTEGER, PARAMETER :: N = 100
      REAL :: T(N,N), TNEW(N,N)
      INTEGER :: I, J

      T = 0.0
      TNEW = 0.0

      DO I = 1, N
         T(I,1) = 100.0
      END DO

      DO J = 1, 1000
         DO I = 2, N-1
            TNEW(I,1) = T(I-1,1) + T(I+1,1)
         END DO
         T = TNEW
      END DO

      WRITE (*,*) T
      END PROGRAM HEAT_EQ