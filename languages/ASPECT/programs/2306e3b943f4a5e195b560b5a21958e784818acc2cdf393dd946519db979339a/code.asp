; FIBONACCI.ASP - Fibonacci sequence calculator
; ProComm Plus ASPECT scripting language
; Displays the first 10 Fibonacci numbers

PROC MAIN
  INTEGER A
  INTEGER B
  INTEGER TEMP
  INTEGER COUNT

  A = 0
  B = 1
  COUNT = 0

  PRINTS "Fibonacci Sequence"
  PRINTS "------------------"

  WHILE COUNT < 10
    PRINTS A
    TEMP = B
    B = A + B
    A = TEMP
    COUNT = COUNT + 1
  ENDWHILE

ENDPROC