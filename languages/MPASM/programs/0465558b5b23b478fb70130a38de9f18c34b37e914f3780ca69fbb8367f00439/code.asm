; LED Blink for PIC16F84A using MPASM Assembler
; Toggles RB0 with a software delay loop

    list        p=16f84a
    #include    <p16f84a.inc>

    __CONFIG    _CP_OFF & _WDT_OFF & _XT_OSC & _PWRTE_ON

; General-purpose registers in Bank 0 user RAM
    CBLOCK  0x0C
COUNT1          ; inner delay counter
COUNT2          ; outer delay counter
    ENDC

;-----------------------------------------------------------
    ORG     0x000           ; Reset vector
    nop
    goto    Start

    ORG     0x004           ; Interrupt vector (unused)
    retfie

    ORG     0x005
;-----------------------------------------------------------
Start:
    bsf     STATUS, RP0     ; Select Bank 1
    clrf    TRISB           ; PORTB all outputs
    bcf     STATUS, RP0     ; Back to Bank 0
    clrf    PORTB           ; All pins low

MainLoop:
    bsf     PORTB, 0        ; RB0 high (LED on)
    call    Delay
    bcf     PORTB, 0        ; RB0 low (LED off)
    call    Delay
    goto    MainLoop

;-----------------------------------------------------------
; Delay: approx 250 ms at 4 MHz crystal
;-----------------------------------------------------------
Delay:
    movlw   d'250'
    movwf   COUNT2
DelayOuter:
    movlw   d'250'
    movwf   COUNT1
DelayInner:
    decfsz  COUNT1, F
    goto    DelayInner
    decfsz  COUNT2, F
    goto    DelayOuter
    return

    END
