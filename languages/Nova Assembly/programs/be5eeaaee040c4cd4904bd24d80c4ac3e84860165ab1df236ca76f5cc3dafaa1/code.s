; Nova Assembly - Hello World Program
; Output "HELLO" to the teletype

        .TITL   HELLO

START:  LDA     0,MSG   ; Load address of message
        STA     0,PTR   ; Store in pointer

LOOP:   LDA     0,@PTR  ; Load character from message
        SNZ             ; Skip if not zero
        JMP     DONE    ; Done if zero
        JSR     PUTC    ; Output character
        ISZ     PTR     ; Increment pointer
        JMP     LOOP    ; Continue loop

DONE:   HALT

; Subroutine to output a character
PUTC:   SKPDO           ; Skip if device done
        JMP     .-1     ; Wait for ready
        DOA     0,TTY   ; Output character to TTY
        JMP     0,3     ; Return

; Data
MSG:    .BLKW   1       ; Message pointer
PTR:    .WORD   'H
        .WORD   'E
        .WORD   'L
        .WORD   'L
        .WORD   'O
        .WORD   0       ; Null terminator

TTY:    .EQU    10      ; Teletype device code
