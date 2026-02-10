; Simple 6502 Assembly program
; Adds two numbers and stores result

LDA #$05        ; Load accumulator with 5
CLC             ; Clear carry flag
ADC #$03        ; Add 3 to accumulator
STA $0200       ; Store result at memory location $0200
BRK             ; Break (end program)
