/ TX-2 Assembly - Simple Counter Program
/ This program counts from 1 to 10
/
        CLA             / Clear accumulator
        TAD TEN         / Load 10 into AC
        DCA COUNT       / Store in COUNT
LOOP,   TAD COUNT       / Load COUNT
        CIA             / Complement and increment
        SNA             / Skip if AC not zero
        HLT             / Halt if zero
        TAD COUNT       / Load COUNT
        TAD MONE        / Subtract 1
        DCA COUNT       / Store back
        JMP LOOP        / Jump to LOOP
TEN,    10              / Constant 10
MONE,   -1              / Constant -1
COUNT,  0               / Counter variable
