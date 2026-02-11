LD 1
ST Index
Loop:
LD Index
LE 10
JMPC EndLoop
LD Result
ADD Index
ST Result
LD Index
ADD 1
ST Index
JMP Loop
EndLoop: