; Hello World program for Motorola 6809
; Outputs "Hello, World!" to console

        ORG     $0100           ; Program starts at $0100

START   LDX     #MESSAGE        ; Load X with address of message
LOOP    LDA     ,X+             ; Load A with byte at X, increment X
        BEQ     DONE            ; If zero, we're done
        JSR     PUTCHAR         ; Output character
        BRA     LOOP            ; Continue loop
DONE    RTS                     ; Return to operating system

MESSAGE FCC     "Hello, World!"
        FCB     $0D,$0A,$00     ; CR, LF, null terminator

PUTCHAR EQU     $A000           ; Character output routine address
        END     START
