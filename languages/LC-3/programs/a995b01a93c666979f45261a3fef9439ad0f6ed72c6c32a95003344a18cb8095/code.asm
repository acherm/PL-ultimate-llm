; LC-3 Assembly Program - Add Two Numbers
; This program adds two numbers stored in memory
; and stores the result in another memory location

.ORIG x3000

; Load first number into R1
LD R1, NUM1

; Load second number into R2
LD R2, NUM2

; Add R1 and R2, store result in R3
ADD R3, R1, R2

; Store result
ST R3, RESULT

; Halt the program
HALT

; Data section
NUM1    .FILL #5
NUM2    .FILL #7
RESULT  .BLKW 1

.END