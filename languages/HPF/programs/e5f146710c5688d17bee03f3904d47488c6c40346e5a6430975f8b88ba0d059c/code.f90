PROGRAM VectorAdd
  IMPLICIT NONE
  INTEGER, PARAMETER :: N = 100
  REAL, DIMENSION(N) :: A, B, C
  INTEGER :: I
  !HPF$ DISTRIBUTE A(BLOCK)
  !HPF$ DISTRIBUTE B(BLOCK)
  !HPF$ DISTRIBUTE C(BLOCK)

  ! Initialize arrays
  FORALL (I = 1:N) A(I) = REAL(I)
  FORALL (I = 1:N) B(I) = REAL(N + 1 - I)

  ! Parallel element-wise addition
  C = A + B

  PRINT *, 'First element:', C(1)
  PRINT *, 'Last element:', C(N)
END PROGRAM VectorAdd
