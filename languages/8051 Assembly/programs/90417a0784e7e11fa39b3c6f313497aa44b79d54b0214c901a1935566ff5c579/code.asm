; 8051 Assembly - LED Blink Program
; Blinks an LED connected to P1.0

ORG 0000H           ; Start at address 0000H
    LJMP MAIN       ; Jump to main program

ORG 0030H           ; Main program starts at 0030H
MAIN:
    MOV P1, #00H    ; Initialize Port 1 to 0

LOOP:
    SETB P1.0       ; Turn on LED at P1.0
    ACALL DELAY     ; Call delay subroutine
    CLR P1.0        ; Turn off LED at P1.0
    ACALL DELAY     ; Call delay subroutine
    SJMP LOOP       ; Repeat forever

DELAY:
    MOV R7, #250    ; Outer loop counter
DEL1:
    MOV R6, #250    ; Inner loop counter
DEL2:
    DJNZ R6, DEL2   ; Decrement R6, jump if not zero
    DJNZ R7, DEL1   ; Decrement R7, jump if not zero
    RET             ; Return from subroutine

END
