; DLX Assembly - Factorial of 5
; Computes 5! = 120

        .data
result: .word 0

        .text
        .global main

main:
        ; Initialize registers
        addi r1, r0, 5      ; n = 5
        addi r2, r0, 1      ; result = 1

factorial_loop:
        ; Check if n <= 0
        seqi r3, r1, 0      ; r3 = (n == 0)
        bnez r3, done       ; if n == 0, exit loop

        ; result = result * n
        mult r2, r2, r1     ; result *= n

        ; n = n - 1
        subi r1, r1, 1      ; n--

        ; Continue loop
        j factorial_loop

done:
        ; Store result in memory
        sw result, r2

        ; Exit
        trap 0
