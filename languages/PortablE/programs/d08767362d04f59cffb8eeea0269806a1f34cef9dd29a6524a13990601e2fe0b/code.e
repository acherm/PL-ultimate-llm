PROC fib(n)
  IF n <= 1 THEN RETURN n
  RETURN fib(n-1) + fib(n-2)
ENDPROC

PROC main()
  DEF i
  FOR i := 0 TO 10
    WriteF('fib(\d) = \d\n', i, fib(i))
  ENDFOR
ENDPROC
