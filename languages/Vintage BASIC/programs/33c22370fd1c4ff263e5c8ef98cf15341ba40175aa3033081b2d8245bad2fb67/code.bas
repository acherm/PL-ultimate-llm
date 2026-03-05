10 REM Guess the number game in Vintage BASIC
20 RANDOMIZE
30 LET S = INT(RND(1) * 100) + 1
40 LET G = 0
50 PRINT "I am thinking of a number between 1 and 100."
60 INPUT "Your guess"; N
70 LET G = G + 1
80 IF N < S THEN PRINT "Too low!" : GOTO 60
90 IF N > S THEN PRINT "Too high!" : GOTO 60
100 PRINT "Correct! You got it in"; G; "guesses."
110 END
