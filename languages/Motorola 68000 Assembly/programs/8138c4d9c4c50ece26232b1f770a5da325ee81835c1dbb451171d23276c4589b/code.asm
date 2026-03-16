; Hello World in Motorola 68000 Assembly
; Assembled with EASy68K simulator

        ORG     $1000

START:
        MOVE.B  #14,D0          ; task 14 = display null-terminated string
        LEA     MSG,A1          ; A1 points to message
        TRAP    #15             ; call Easy68K OS trap

        MOVE.B  #9,D0           ; task 9 = halt program
        TRAP    #15

MSG:    DC.B    'Hello, World!',0

        END     START
