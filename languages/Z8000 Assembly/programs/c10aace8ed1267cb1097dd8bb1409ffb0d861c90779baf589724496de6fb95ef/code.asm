; Z8000 Assembly - Simple string output program
; This program demonstrates basic Z8000 assembly syntax

        .org    $1000           ; Origin at address $1000

start:
        ldl     rr2,#message    ; Load address of message into register pair rr2
        ld      r4,#msglen      ; Load message length into r4

loop:
        ldb     rl0,(rr2)       ; Load byte from memory pointed by rr2 into rl0
        outb    $FE,rl0         ; Output byte to I/O port $FE
        inc     r2,#1           ; Increment address pointer
        djnz    r4,loop         ; Decrement r4 and jump if not zero

        halt                    ; Halt execution

message:
        .byte   "Hello from Z8000!",13,10
msglen  .equ    *-message       ; Calculate message length
