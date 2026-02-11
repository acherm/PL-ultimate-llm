/ PDP-4 Assembly: Simple addition program
/ Load two numbers and add them

START,  CLA         / Clear accumulator
        TAD NUM1    / Add NUM1 to accumulator
        TAD NUM2    / Add NUM2 to accumulator
        DCA RESULT  / Deposit and clear accumulator to RESULT
        HLT         / Halt

NUM1,   0012        / First number (octal 12 = decimal 10)
NUM2,   0015        / Second number (octal 15 = decimal 13)
RESULT, 0000        / Result storage
