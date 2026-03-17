; Fibonacci sequence in RGBDS Game Boy Assembly (RGBASM)
; Computes successive Fibonacci numbers using WRAM variables

SECTION "Variables", WRAM0

FibPrev:    ds 1    ; Previous Fibonacci number
FibCurr:    ds 1    ; Current Fibonacci number

SECTION "Main", ROM0[$150]

Main::
    ; Initialize: fib(0)=0, fib(1)=1
    xor a
    ld [FibPrev], a     ; FibPrev = 0
    inc a
    ld [FibCurr], a     ; FibCurr = 1

    ld c, 8             ; Compute 8 more iterations

.loop:
    ld a, [FibPrev]     ; a = FibPrev
    ld b, a             ; b = FibPrev (save it)
    ld a, [FibCurr]     ; a = FibCurr
    ld [FibPrev], a     ; FibPrev = old FibCurr
    add a, b            ; a = old FibCurr + old FibPrev
    ld [FibCurr], a     ; FibCurr = sum

    dec c
    jr nz, .loop        ; Repeat 8 times

    ; FibCurr now holds fib(9) = 34

.done:
    halt
    nop
    jr .done
