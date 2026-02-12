* CDC 6600 Assembly Program - Add Two Numbers
* This program demonstrates basic arithmetic
         ORG   0
START    LDX   A
         ADX   B
         STX   C
         HALT
A        DATA  5
B        DATA  7
C        BSS   1
         END   START