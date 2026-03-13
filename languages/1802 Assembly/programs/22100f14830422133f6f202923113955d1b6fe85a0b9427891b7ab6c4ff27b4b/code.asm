; RCA 1802 Assembly - Fibonacci Sequence
; Computes first 10 Fibonacci numbers (8-bit) and stores to memory
; Assembles with standard RCA 1802 assembler syntax

        ORG  0000H

; Memory layout:
;   0000H: Program code
;   0100H: Result buffer (10 bytes)
;
; Register use:
;   R0 = program counter (P=0)
;   R2 = memory pointer (X=2), also result pointer
;   R4 = F(n-1), previous Fibonacci number
;   R5 = F(n),   current Fibonacci number
;   R6 = loop counter
;   R7 = temporary (F(n+1))

        LDI  01H        ; Load high byte of result address
        PHI  R2
        LDI  00H        ; Load low byte of result address
        PLO  R2         ; R2 = 0100H

        SEX  R2         ; Set X = 2 (memory operations via R2)

        LDI  00H
        PLO  R4         ; R4 = 0 (first Fibonacci number)
        LDI  01H
        PLO  R5         ; R5 = 1 (second Fibonacci number)
        LDI  0AH
        PLO  R6         ; R6 = 10 (loop count)

LOOP:   GLO  R4         ; D = F(n-1)
        STR  R2         ; Store F(n-1) to result buffer
        INC  R2         ; Advance result pointer

        GLO  R4         ; D = F(n-1)
        STR  R2         ; Temp: store F(n-1) at M(R2)
        GLO  R5         ; D = F(n)
        ADD             ; D = F(n) + M(R2) = F(n) + F(n-1) = F(n+1)
        PLO  R7         ; Save F(n+1) in R7

        GLO  R5
        PLO  R4         ; R4 = old F(n) [becomes new F(n-1)]
        GLO  R7
        PLO  R5         ; R5 = F(n+1) [becomes new F(n)]

        DEC  R6         ; Decrement counter
        GLO  R6         ; Load counter into D
        BNZ  LOOP       ; Branch if counter not zero

        IDL             ; Halt (wait for interrupt)

        END
