10 CLS
20 PRINT "Number Guessing Game"
30 PRINT "I'm thinking of a number between 1 and 100"
40 N = INT(RND * 100) + 1
50 G = 0
60 INPUT "Your guess"; A
70 G = G + 1
80 IF A = N THEN 130
90 IF A < N THEN PRINT "Too low!"
100 IF A > N THEN PRINT "Too high!"
110 GOTO 60
120 REM Victory condition
130 PRINT "Correct! You got it in"; G; "guesses!"
140 END
