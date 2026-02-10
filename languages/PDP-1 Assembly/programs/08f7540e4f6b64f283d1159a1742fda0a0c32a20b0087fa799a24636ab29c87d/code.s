/ Simple PDP-1 Assembly program to add two numbers
/ This program adds the values at locations A and B
/ and stores the result in location C

START,  CLA         / Clear accumulator
        LAC A       / Load accumulator with value at A
        ADD B       / Add value at B to accumulator
        DAC C       / Deposit accumulator in C
        HLT         / Halt

A,      10          / First number (octal)
B,      20          / Second number (octal)
C,      0           / Result storage

        END START