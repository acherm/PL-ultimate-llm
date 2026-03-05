; Hello World for CP/M using ZMAC assembler
; Demonstrates ZMAC macro definition and usage

BDOS    EQU     5           ; CP/M BDOS entry point
PSTRING EQU     9           ; Print string function

; Macro to call a BDOS function with a DE argument
BDOSCALL MACRO  FN, ARG
        LD      C, FN
        LD      DE, ARG
        CALL    BDOS
        ENDM

        ORG     100H        ; CP/M TPA start address

START:
        BDOSCALL PSTRING, HELLO
        RET                 ; Return to CP/M

HELLO:  DEFM    'Hello, World!'
        DEFB    13, 10, '$' ; CR, LF, string terminator

        END     START
