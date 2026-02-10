; LED Blink for ATmega328P
; Blinks LED on PB5 (Arduino pin 13)

.include "m328pdef.inc"

.org 0x0000
    rjmp reset

reset:
    ; Set PB5 as output
    ldi r16, 0b00100000
    out DDRB, r16

main_loop:
    ; Turn LED on
    sbi PORTB, 5
    rcall delay
    
    ; Turn LED off
    cbi PORTB, 5
    rcall delay
    
    rjmp main_loop

delay:
    ; Simple delay loop
    ldi r18, 41
outer:
    ldi r19, 0
middle:
    ldi r20, 0
inner:
    dec r20
    brne inner
    dec r19
    brne middle
    dec r18
    brne outer
    ret
