; MSP430 LED Blink Program
; Blinks LED on P1.0
; Target: MSP430G2553

.cdecls C,LIST,"msp430.h"

    .text
    .global _start

_start:
    ; Stop watchdog timer
    mov.w   #WDTPW|WDTHOLD, &WDTCTL

    ; Set P1.0 as output
    bis.b   #BIT0, &P1DIR

main_loop:
    ; Toggle P1.0
    xor.b   #BIT0, &P1OUT

    ; Delay loop
    mov.w   #0xFFFF, R15
delay:
    dec.w   R15
    jnz     delay

    ; Repeat
    jmp     main_loop

    .end