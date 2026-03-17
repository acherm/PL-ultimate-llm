-- R:BASE command file: Fibonacci sequence
-- Demonstrates SET VAR, WHILE loop, and WRITE commands

SET VAR vA INTEGER = 0
SET VAR vB INTEGER = 1
SET VAR vTemp INTEGER = 0
SET VAR vCount INTEGER = 1

WRITE 'Fibonacci Sequence (first 10 terms):'
WHILE #vCount <= 10 THEN
  WRITE 'F(' & CTXT(#vCount) & ') = ' & CTXT(#vA)
  SET VAR vTemp INTEGER = #vA + #vB
  SET VAR vA INTEGER = #vB
  SET VAR vB INTEGER = #vTemp
  SET VAR vCount INTEGER = #vCount + 1
ENDWHILE

WRITE 'Calculation complete.'
