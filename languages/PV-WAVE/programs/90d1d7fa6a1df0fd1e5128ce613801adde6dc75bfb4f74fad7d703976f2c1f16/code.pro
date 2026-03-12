; Fibonacci sequence in PV-WAVE
PRO fibonacci, n
  a = 0UL
  b = 1UL
  FOR i = 0, n-1 DO BEGIN
    PRINT, a
    t = a + b
    a = b
    b = t
  ENDFOR
END

fibonacci, 15
