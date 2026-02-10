1000 REM BASICODE-2 Example: Sum Calculator
1010 REM This program calculates the sum of numbers
1020 A=390: GOSUB 100
1030 PRINT "Sum Calculator"
1040 A=392: GOSUB 100
1050 INPUT "Enter first number: "; N1
1060 INPUT "Enter second number: "; N2
1070 S=N1+N2
1080 PRINT "The sum is: "; S
1090 A=395: GOSUB 100
1100 INPUT "Calculate again (Y/N)? "; A$
1110 IF A$="Y" THEN 1040
1120 END
