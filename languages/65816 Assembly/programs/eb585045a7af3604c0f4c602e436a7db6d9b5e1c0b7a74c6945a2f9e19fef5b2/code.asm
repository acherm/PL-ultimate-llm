; 65816 Assembly - 16-bit Addition Example
; Adds two 16-bit numbers and stores the result

.65816                  ; Set 65816 mode
.a16                    ; 16-bit accumulator
.i16                    ; 16-bit index registers

start:
    clc                 ; Clear carry flag
    lda #$1234          ; Load first number (0x1234)
    adc #$5678          ; Add second number (0x5678)
    sta $0000           ; Store result at address $0000

    rtl                 ; Return from subroutine
