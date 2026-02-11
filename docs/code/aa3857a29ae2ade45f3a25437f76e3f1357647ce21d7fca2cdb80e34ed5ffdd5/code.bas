10 PRINT "Fibonacci Sequence Generator"
20 PRINT "How many numbers do you want? ";
30 INPUT N%
40 IF N% < 1 THEN GOTO 20
50 A% = 0
60 B% = 1
70 PRINT A%
80 FOR I% = 2 TO N%
90   C% = A% + B%
100  PRINT C%
110  A% = B%
120  B% = C%
130 NEXT I%
140 END