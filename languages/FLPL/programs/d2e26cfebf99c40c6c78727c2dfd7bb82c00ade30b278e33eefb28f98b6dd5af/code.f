      PROGRAM REVERSE
      IMPLICIT LIST (A-Z)
      L = LIST(1, 2, 3, 4, 5)
      R = NULL
10    IF (L .EQ. NULL) GO TO 20
      R = CONS(HEAD(L), R)
      L = TAIL(L)
      GO TO 10
20    CALL PRINT(R)
      END
