! Factorial calculation in HicEst
REAL :: n, result

WRITE(Text) 'Enter a number: '
READ(Text) n

result = 1
DO i = 1, n
  result = result * i
ENDDO

WRITE(Text) 'Factorial of ', n, ' is ', result
END
