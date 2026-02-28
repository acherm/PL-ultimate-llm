10 INPUT "Please enter your name: ", a$
20 PRINT
30 PRINT "Is your name " a$ " (Y/N) ?"
40 z$ = UPPER$ (INPUT$ (1))
50 IF z$ = "N" THEN 10 : ELSE IF z$ <> "Y" THEN 50
60 PRINT
70 PRINT "Hello, " a$ "!"
